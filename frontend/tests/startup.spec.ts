import { test, expect } from '@playwright/test'

test('首页能通过浏览器连接真实后端', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByRole('heading', { name: '后端连接正常' })).toBeVisible()
    await expect(page.getByRole('button', { name: '重新检查连接' })).toBeEnabled()
})
