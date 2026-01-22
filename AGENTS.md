# Guidelines for Working with AI Assistant Feedback

This repository uses **gemini-code-assist** to provide review suggestions. The assistant may also help in verifying adherence to our unit testing standards for new functions.
Please address all suggestions from the AI assistant. If a suggestion is not implemented, provide a brief justification in the pull request discussion (e.g., as a comment on the pull request itself, or a comment directly on the line of code in question).

Contributors must also follow the workflow and naming rules documented in
[`project-handbook.md`](project-handbook.md) when developing features and creating pull requests.

All new functions must include corresponding unit tests. If unit testing is not feasible for a particular function, a clear explanation should be provided (e.g., as a comment on the pull request itself, or a comment directly on the line of code in question).


## AI 助理審查原則

  * **清晰性與可執行性**：建議將抽象原則具體化為可執行的步驟，以提高指南的清晰度和實用性。
  * **一致性**：審查會指出文件中的不一致之處（例如，檔案命名慣例、Markdown 語法），並建議標準化以提高清晰度和可維護性。
  * **最佳實踐**：Gemini Code Assist 建議遵循網頁最佳實踐（例如，避免 URL 中的空格、可存取的行動裝置導覽）、Python 最佳實踐（例如，使用 numpy.percentile 而非自訂實作、新增 docstring、將錯誤訊息導向 `stderr`），以及一般軟體工程最佳實踐（例如，避免硬式編碼資料、強固的錯誤處理、模組化）。
  * **正確性與強固性**：審查著重於識別潛在錯誤（例如，檔案刪除中的符號連結處理、模擬器中的輸入驗證），確保類型安全和設計一致性，並提高程式碼的整體強固性。
  * **可維護性與可重用性**：建議通常旨在減少程式碼重複、將邏輯集中到可重用元件中，並提高程式碼庫的整體可維護性。
  * **文件品質**：強調清晰、準確且一致的文件，包括改進描述、更正格式以及確保文件與程式碼實作一致的建議。
  * **使用者體驗與無障礙性**：對於與網頁相關的變更，審查會考慮使用者體驗和無障礙性，例如建議更好的導覽模式和描述性頁面標題。
  * **避免不必要的檔案和膨脹**：建議使用 .gitignore 處理暫存檔案和聊天記錄，以防止它們被提交到儲存庫。
  * **結構化規劃**：建議在專用檔案 (IMPROVEMENT_PLAN.md) 中為複雜任務制定詳細的執行計畫，並在工作日誌 (WORKLOG.md) 中記錄操作。
  * **錯誤和失敗處理協定**：提供明確的錯誤處理協定，包括說明事實、診斷原因和提出解決方案，同時避免情緒化語言。
  * **基於事實的現實和誠實的不確定性**：強調輸出應基於可驗證的事實和嚴謹的邏輯推理，並在資訊不足或不確定結論時明確說明。
  * **直接、專業和簡潔的互動風格**：提倡清晰、專業和簡潔的溝通，專注於使用者目標並消除冗餘的對話。
  * **偵測系統中的安全性和準確性**：對於可疑連結偵測等功能，審查會強調準確偵測邏輯的重要性，以避免誤判，並建議改進關鍵字檢查和網域黑名單。
  * **設定一致性**：審查建議將設定定義（例如 `TypedDict`）與範例設定檔（例如 `config.yaml`）對齊，並確保 CLI 參數經過驗證。

# 🛠 專案名稱 - 開發協作手冊

## 📋 目錄
1. [任務分工與進度追蹤](#任務分工與進度追蹤)
2. [Git 開發流程與規範](#git-開發流程與規範)
3. [程式碼撰寫與 Review 注意事項](#程式碼撰寫與-review-注意事項)
4. [每日工作日誌區塊](#每日工作日誌區塊)
5. [資源與文件連結](#資源與文件連結)

---

## 🧱 任務分工與進度追蹤

| 任務編號 | 功能說明             | 負責人 | 狀態         | 備註 |
|----------|----------------------|--------|--------------|------|
| #001     | 登入畫面切版         | A      | ✅ 完成       |      |
| #002     | Google 登入串接      | B      | 🟡 進行中     | 依賴 #001 |
| #003     | API Token 機制       | B      | ⏳ 待開始     |      |

- 狀態建議使用：⏳ 待開始｜🟡 進行中｜🔍 審核中｜✅ 完成

---

## 🌱 Git 開發流程與規範

1. 每項任務請建立 feature branch，例如：
   ```bash
   git checkout -b feature/login-ui
   ```

2. 完成後發起 Pull Request（PR），標題格式：

   ```
   [Feature] 登入頁面切版 (#001)
   ```
3. 不能直接 push 到 `main` 分支，需透過 PR。
4. PR 提交後需指派另一位協作者進行 Review。
5. 合併前務必確認：

   * ✅ 沒有衝突
   * ✅ 已自我測試過
   * ✅ 遵守命名與格式規範

---

## 🧠 程式碼撰寫與 Review 注意事項

### 🧹 命名原則

* 變數需有語意：`userInfo` 不要寫成 `x`
* 函式命名盡量是動詞開頭，如 `getUserInfo`

### 🛡 程式邏輯

* 防呆與錯誤處理要寫清楚（例如登入錯誤的提示）
* 不要留死 code
* API 錯誤時要 console log 錯誤資訊

### 👀 Review 時要看的事

* [ ] 功能是否如預期運作？
* [ ] 是否有不合理命名？
* [ ] 是否有簡化空間或可讀性問題？
* [ ] 有無潛在 Bug（如未處理 null）？
* [ ] 結尾是否有自我測試結果備註？

---

## 🗓 每次工作日誌區塊

> 請每次 commit 前更新一次，記錄格式如下：

```markdown
### 🙋‍♂️ A 的日誌（2025/07/08）
- ✅ 完成：登入畫面切版（#001）
- 🟡 進行中：樣式微調、RWD 修正
- 🤔 問題：尚未確定登入按鈕顏色是否符合設計稿

### 🧑‍💻 B 的日誌（2025/07/08）
- ✅ 完成：API token 的初步設計草圖
- ⏳ 明日計畫：串接登入按鈕與 token API
- 🙋 想問：Login API 回傳錯誤格式是否統一？
```

---

## 📚 資源與文件連結

* 🔗 Figma 設計稿：[點我前往](https://figma.com/xxxx)
* 🔗 API 文件連結：[Swagger Docs](http://localhost:8000/docs)
* 🔗 技術指南 / Code Style：[點我查看](https://github.com/你的組織/code-style-guide)

---

## 📌 補充：兩人協作小叮嚀

* **如果卡住，請互相支援或寫日誌記錄問題點，等老闆回來再補救**
* **分工明確，避免同時改動同一檔案造成衝突**
* **即使只是小改動，也請走 PR 流程，養成良好習慣**

---

## 🏁 TODO 清單樣板（可複製貼上）

```markdown
- [ ] 任務說明：
- [ ] 建立分支：
- [ ] 自我測試情境：
- [ ] 需他人 Review 項目：
- [ ] 文件是否補上：
```

---

## 🧰 建議檔名：`project-handbook.md` 或 `開發協作手冊.md`

---

這樣設計的優點是：

* **透明可見**：不在時，也能清楚該怎麼協作與更新。
* **低門檻維護**：全用文字就能同步，不需額外學工具。
* **便於版本控管**：放在專案根目錄，搭配 Git 使用。
