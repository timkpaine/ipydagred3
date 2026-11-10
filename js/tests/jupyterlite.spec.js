import { readFileSync } from "node:fs";
import { expect, test } from "@playwright/test";

const version = readFileSync("../pyproject.toml", "utf8").match(/^version = "([^"]+)"/m)[1];

test("opens examples.ipynb by default and runs it with the Pyodide kernel", async ({
  page,
}, testInfo) => {
  const wheels = [];
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("response", (response) => {
    if (response.url().includes("/pypi/ipydagred3-") && response.status() === 200)
      wheels.push(response.url());
  });
  await page.goto("/lite/");
  await expect(page.getByRole("tab", { name: /examples.ipynb/ })).toBeVisible({ timeout: 120_000 });
  const notebook = page.locator(".jp-NotebookPanel:visible .jp-Notebook");
  await expect(notebook).toBeVisible({ timeout: 120_000 });
  await expect(
    page.getByRole("button", { name: "Python (Pyodide) | Idle", exact: true }),
  ).toBeVisible({ timeout: 120_000 });
  if (testInfo.project.name === "firefox-no-jspi") {
    const worker = page.workers().find((worker) => worker.url().includes("comlink.worker"));
    expect(await worker.evaluate(() => typeof WebAssembly.Suspending)).toBe("undefined");
  }
  await notebook.locator(".jp-Cell").first().click();
  await page.getByRole("menuitem", { name: "Run", exact: true }).click();
  await page.getByRole("menuitem", { name: "Run All Cells", exact: true }).click();
  await expect(notebook.getByText(`ipydagred3 ${version}`, { exact: true })).toBeVisible({
    timeout: 240_000,
  });

  const network = notebook
    .locator(".jp-CodeCell")
    .filter({ hasText: "network_widget = DagreD3Widget" })
    .locator("spaday-dagre");
  await expect(network.locator('[data-node-id="test2"]')).toBeVisible({ timeout: 60_000 });
  const edge = network.locator(
    '[data-edge-source="test"][data-edge-target="test2"] .spaday-dagre-edge-line',
  );
  await expect(edge).toHaveAttribute("d", /^M/);
  expect(await edge.evaluate((path) => path.getTotalLength())).toBeGreaterThan(0);
  const tooltips = notebook
    .locator(".jp-CodeCell")
    .filter({ hasText: "tooltip_box = VBox" })
    .locator("spaday-dagre");
  await expect(tooltips.locator('[data-node-id="d"]')).toBeVisible();
  await expect(tooltips.locator('[data-edge-source="b"][data-edge-target="d"]')).toBeVisible();
  await tooltips.locator('[data-node-id="b"]').click();
  await expect(notebook.getByText("last clicked: b", { exact: true })).toBeVisible();

  await expect(
    page.getByRole("button", { name: "Python (Pyodide) | Idle", exact: true }),
  ).toBeVisible();
  await expect(notebook.locator(".jp-OutputArea-error")).toHaveCount(0);
  const stderr = await notebook
    .locator('[data-mime-type="application/vnd.jupyter.stderr"]')
    .allTextContents();
  expect(stderr.filter((text) => /Error|Traceback/.test(text))).toEqual([]);
  expect(errors).toEqual([]);
  expect(wheels.some((url) => url.includes(`ipydagred3-${version}-`))).toBe(true);
});
