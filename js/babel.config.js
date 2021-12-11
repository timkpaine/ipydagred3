/******************************************************************************
 *
 * Copyright (c) 2020, the ipydagred3 authors.
 *
 * This file is part of the ipydagred3 library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
module.exports = {
  presets: [
    [
      "@babel/preset-env",
      {
        targets: {
          node: "current",
        },
      },
    ],
  ],
};
