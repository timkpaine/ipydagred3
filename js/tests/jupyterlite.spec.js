import { readFileSync } from "node:fs";
import { expect, test } from "@playwright/test";

const version = readFileSync("../pyproject.toml", "utf8").match(/^version = "([^"]+)"/m)[1];

for (const example of ["example", "tooltip"]) {
  test(`${example} runs in JupyterLite with the freshly built wheel`, async ({ page }) => {
    const wheels = [];
    page.on("response", (response) => {
      if (response.url().includes("/pypi/ipydagred3-") && response.status() === 200)
        wheels.push(response.url());
    });
    await page.goto(`/lite/lab/index.html?path=${example}.ipynb`);
    const notebook = page.locator(".jp-NotebookPanel:visible .jp-Notebook");
    await expect(notebook).toBeVisible({ timeout: 180_000 });
    await notebook.locator(".jp-Cell").first().click();
    const count = await notebook.locator(".jp-Cell").count();
    for (let i = 0; i < count; i++) await page.keyboard.press("Shift+Enter");
    await expect(notebook.getByText(`ipydagred3 ${version}`, { exact: true })).toBeVisible({
      timeout: 240_000,
    });
    const graph = notebook.locator("spaday-dagre");
    await expect(graph.locator("svg")).toBeVisible({ timeout: 60_000 });
    if (example === "tooltip") {
      await expect(graph.locator('[data-node-id="d"]')).toBeVisible();
      await expect(graph.locator('[data-edge-source="b"][data-edge-target="d"]')).toBeVisible();
      await graph.locator('[data-node-id="b"]').click();
      await expect(notebook.getByText("last clicked: b", { exact: true })).toBeVisible();
    } else {
      await expect(graph.locator('[data-node-id="test2"]')).toBeVisible();
      const edge = graph.locator(
        '[data-edge-source="test"][data-edge-target="test2"] .spaday-dagre-edge-line',
      );
      await expect(edge).toHaveAttribute("d", /^M/);
      expect(await edge.evaluate((path) => path.getTotalLength())).toBeGreaterThan(0);
    }
    await expect(
      page.getByRole("button", { name: "Python (Pyodide) | Idle", exact: true }),
    ).toBeVisible();
    await expect(notebook.locator(".jp-OutputArea-error")).toHaveCount(0);
    const stderr = await notebook
      .locator('[data-mime-type="application/vnd.jupyter.stderr"]')
      .allTextContents();
    expect(stderr.filter((text) => /Error|Traceback/.test(text))).toEqual([]);
    expect(wheels.some((url) => url.includes(`ipydagred3-${version}-`))).toBe(true);
  });
}
