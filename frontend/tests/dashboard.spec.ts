import { expect, test } from "@playwright/test";

test("shows the QA dashboard", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Test Execution Dashboard" })).toBeVisible();
  await expect(page.getByText("Regression status")).toBeVisible();
});
