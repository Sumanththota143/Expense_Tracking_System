
const API_BASE = "";

// ============================================================
// APPLICATION STATE
// ============================================================

let currentExpenses = [];

let editingExpenseId = null;

// ============================================================
// DOM ELEMENTS
// ============================================================

const expenseDate =
document.getElementById("expenseDate");

const formDate =
document.getElementById("formDate");

const loadBtn =
document.getElementById("loadBtn");

const refreshBtn =
document.getElementById("refreshBtn");

const expenseForm =
document.getElementById("expenseForm");

const tableBody =
document.getElementById("expenseTableBody");

const totalAmount =
document.getElementById("totalAmount");

const transactionCount =
document.getElementById("transactionCount");

const averageAmount =
document.getElementById("averageAmount");

const categoryCount =
document.getElementById("categoryCount");

const categoryList =
document.getElementById("categoryList");

const selectedDateText =
document.getElementById("selectedDateText");

const messageBox =
document.getElementById("messageBox");

const amountInput =
document.getElementById("amount");

const categoryInput =
document.getElementById("category");

const notesInput =
document.getElementById("notes");

const submitButton =
document.getElementById("submitExpenseBtn");

const cancelEditBtn =
document.getElementById("cancelEditBtn");

const formTitle =
document.getElementById("formTitle");

const formDescription =
document.getElementById("formDescription");

const addExpenseCard =
document.getElementById("add-expense");

// ============================================================
// INITIALIZATION
// ============================================================

function initialize() {

const today =
    new Date();

const todayString =
    today.toISOString()
        .split("T")[0];

expenseDate.value =
    todayString;

formDate.value =
    todayString;

loadExpenses();

}

// ============================================================
// CURRENCY FORMAT
// ============================================================

function formatCurrency(value) {

return new Intl.NumberFormat(
    "en-IN",
    {
        style: "currency",
        currency: "INR",
        minimumFractionDigits: 2
    }
).format(value);

}

// ============================================================
// DATE FORMAT
// ============================================================

function formatDate(dateString) {

if (!dateString) {

    return "-";

}

const date =
    new Date(
        `${dateString}T00:00:00`
    );

return date.toLocaleDateString(
    "en-IN",
    {
        day: "2-digit",
        month: "short",
        year: "numeric"
    }
);

}

// ============================================================
// HTML ESCAPE
// ============================================================

function escapeHtml(value) {

if (
    value === null ||
    value === undefined
) {

    return "";

}

return String(value)

    .replaceAll(
        "&",
        "&amp;"
    )

    .replaceAll(
        "<",
        "&lt;"
    )

    .replaceAll(
        ">",
        "&gt;"
    )

    .replaceAll(
        '"',
        "&quot;"
    )

    .replaceAll(
        "'",
        "&#039;"
    );

}

// ============================================================
// SHOW MESSAGE
// ============================================================

function showMessage(
message,
type = "success"
) {

messageBox.textContent =
    message;

messageBox.className =
    `message ${type}`;

setTimeout(
    () => {

        messageBox.classList.add(
            "hidden"
        );

    },
    4000
);

}

// ============================================================
// LOAD EXPENSES
// ============================================================

async function loadExpenses() {

const date =
    expenseDate.value;

if (!date) {

    showMessage(
        "Please select a date.",
        "error"
    );

    return;

}

tableBody.innerHTML = `
    <tr>
        <td
            colspan="6"
            class="empty-state"
        >
            Loading expenses...
        </td>
    </tr>
`;

try {

    const response =
        await fetch(
            `${API_BASE}/expenses/${date}`
        );

    if (!response.ok) {

        throw new Error(
            `HTTP ${response.status}`
        );

    }

    const data =
        await response.json();

    currentExpenses =
        Array.isArray(data)
            ? data
            : [];

    renderExpenses(
        currentExpenses
    );

    updateStatistics(
        currentExpenses
    );

    updateCategories(
        currentExpenses
    );

    selectedDateText.textContent =
        `Expenses for ${formatDate(date)}`;

} catch (error) {

    console.error(
        "Load error:",
        error
    );

    currentExpenses = [];

    renderExpenses([]);

    updateStatistics([]);

    updateCategories([]);

    showMessage(
        "Unable to load expenses. Check that FastAPI is running.",
        "error"
    );

}

}

// ============================================================
// RENDER EXPENSE TABLE
// ============================================================

function renderExpenses(expenses) {

if (
    !expenses ||
    expenses.length === 0
) {

    tableBody.innerHTML = `
        <tr>
            <td
                colspan="6"
                class="empty-state"
            >
                No expenses found for this date.
            </td>
        </tr>
    `;

    return;

}

tableBody.innerHTML =
    expenses
        .map(
            expense => {

                return `
                    <tr>

                        <td>
                            #${escapeHtml(
                                expense.id
                            )}
                        </td>

                        <td>
                            ${formatDate(
                                expense.expense_date
                            )}
                        </td>

                        <td>

                            <span
                                class="category-badge"
                            >
                                ${escapeHtml(
                                    expense.category
                                )}
                            </span>

                        </td>

                        <td>
                            ${escapeHtml(
                                expense.notes || "-"
                            )}
                        </td>

                        <td class="amount">

                            ${formatCurrency(
                                Number(
                                    expense.amount
                                )
                            )}

                        </td>

                        <td>

                            <div
                                class="action-buttons"
                            >

                                <button
                                    type="button"
                                    class="edit-btn"
                                    onclick="editExpense(${expense.id})"
                                >
                                    Edit
                                </button>

                                <button
                                    type="button"
                                    class="delete-btn"
                                    onclick="deleteExpense(${expense.id})"
                                >
                                    Delete
                                </button>

                            </div>

                        </td>

                    </tr>
                `;

            }
        )
        .join("");

}

// ============================================================
// UPDATE STATISTICS
// ============================================================

function updateStatistics(
expenses
) {

const total =
    expenses.reduce(
        (
            sum,
            expense
        ) => {

            return (
                sum +
                Number(
                    expense.amount || 0
                )
            );

        },
        0
    );

const count =
    expenses.length;

const average =
    count > 0
        ? total / count
        : 0;

const categories =
    new Set(
        expenses.map(
            expense =>
                expense.category
        )
    );

totalAmount.textContent =
    formatCurrency(total);

transactionCount.textContent =
    count;

averageAmount.textContent =
    formatCurrency(average);

categoryCount.textContent =
    categories.size;

}

// ============================================================
// CATEGORY BREAKDOWN
// ============================================================

function updateCategories(
expenses
) {

if (
    !expenses ||
    expenses.length === 0
) {

    categoryList.innerHTML = `
        <div class="empty-category">
            No data available
        </div>
    `;

    return;

}

const categoryTotals = {};

expenses.forEach(
    expense => {

        const category =
            expense.category ||
            "Other";

        const amount =
            Number(
                expense.amount || 0
            );

        if (
            !categoryTotals[category]
        ) {

            categoryTotals[category] =
                0;

        }

        categoryTotals[category] +=
            amount;

    }
);

const total =
    Object.values(
        categoryTotals
    ).reduce(
        (
            sum,
            value
        ) =>
            sum + value,
        0
    );

const sortedCategories =
    Object.entries(
        categoryTotals
    )
    .sort(
        (
            a,
            b
        ) =>
            b[1] - a[1]
    );

categoryList.innerHTML =
    sortedCategories
        .map(
            (
                [
                    category,
                    amount
                ]
            ) => {

                const percentage =
                    total > 0
                        ? (
                            amount /
                            total
                        ) * 100
                        : 0;

                return `
                    <div
                        class="category-item"
                    >

                        <div
                            class="category-row"
                        >

                            <span
                                class="category-name"
                            >
                                ${escapeHtml(
                                    category
                                )}
                            </span>

                            <span
                                class="category-value"
                            >
                                ${formatCurrency(
                                    amount
                                )}
                            </span>

                        </div>

                        <div
                            class="progress"
                        >

                            <div
                                class="progress-bar"
                                style="width: ${percentage}%"
                            ></div>

                        </div>

                    </div>
                `;

            }
        )
        .join("");

}

// ============================================================
// SUBMIT FORM
// ============================================================

async function submitExpense(
event
) {

event.preventDefault();

const date =
    formDate.value;

const amount =
    Number(
        amountInput.value
    );

const category =
    categoryInput.value;

const notes =
    notesInput.value.trim();

// --------------------------------------------------------
// VALIDATION
// --------------------------------------------------------

if (!date) {

    showMessage(
        "Please select a date.",
        "error"
    );

    return;

}

if (
    !amount ||
    amount <= 0
) {

    showMessage(
        "Please enter a valid amount.",
        "error"
    );

    return;

}

if (!category) {

    showMessage(
        "Please select a category.",
        "error"
    );

    return;

}

if (!notes) {

    showMessage(
        "Please enter notes.",
        "error"
    );

    return;

}

const expense = {

    expense_date:
        date,

    amount:
        amount,

    category:
        category,

    notes:
        notes

};

try {

    let response;

    // ====================================================
    // EDIT
    // ====================================================

    if (
        editingExpenseId !== null
    ) {

        response =
            await fetch(
                `${API_BASE}/expenses/${editingExpenseId}`,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            expense
                        )
                }
            );

    }

    // ====================================================
    // ADD
    // ====================================================

    else {

        response =
            await fetch(
                `${API_BASE}/expenses`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            expense
                        )
                }
            );

    }

    // ====================================================
    // RESPONSE CHECK
    // ====================================================

    if (!response.ok) {

        const errorText =
            await response.text();

        throw new Error(
            errorText
        );

    }

    const result =
        await response.json();

    console.log(
        "API response:",
        result
    );

    // ====================================================
    // SUCCESS
    // ====================================================

    if (
        editingExpenseId !== null
    ) {

        showMessage(
            "Expense updated successfully.",
            "success"
        );

    } else {

        showMessage(
            "Expense added successfully.",
            "success"
        );

    }

    // ====================================================
    // RESET
    // ====================================================

    resetForm();

    // ====================================================
    // SELECT THE DATE THAT WAS SUBMITTED
    // ====================================================

    expenseDate.value =
        date;

    formDate.value =
        date;

    // ====================================================
    // RELOAD
    // ====================================================

    await loadExpenses();

} catch (error) {

    console.error(
        "Save error:",
        error
    );

    showMessage(
        "Unable to save the expense.",
        "error"
    );

}

}

// ============================================================
// EDIT EXPENSE
// ============================================================

function editExpense(id) {

const expense =
    currentExpenses.find(
        item =>
            Number(item.id) ===
            Number(id)
    );

if (!expense) {

    showMessage(
        "Expense could not be found.",
        "error"
    );

    return;

}

editingExpenseId =
    Number(id);

// Fill form

formDate.value =
    expense.expense_date;

amountInput.value =
    expense.amount;

categoryInput.value =
    expense.category;

notesInput.value =
    expense.notes;

// Change form title

formTitle.textContent =
    `Edit Expense #${id}`;

formDescription.textContent =
    "Update the selected expense.";

// Change submit button

submitButton.textContent =
    "Update Expense";

// Show cancel button

cancelEditBtn.classList.remove(
    "hidden"
);

// Add visual editing state

addExpenseCard.classList.add(
    "editing-mode"
);

// Scroll to form

addExpenseCard.scrollIntoView({
    behavior: "smooth",
    block: "center"
});

}

// ============================================================
// DELETE EXPENSE
// ============================================================

async function deleteExpense(id) {

const expense =
    currentExpenses.find(
        item =>
            Number(item.id) ===
            Number(id)
    );

if (!expense) {

    showMessage(
        "Expense could not be found.",
        "error"
    );

    return;

}

const confirmed =
    confirm(
        `Are you sure you want to delete this expense?\n\n` +
        `ID: #${id}\n` +
        `Category: ${expense.category}\n` +
        `Amount: ${formatCurrency(
            Number(expense.amount)
        )}\n` +
        `Notes: ${expense.notes}`
    );

if (!confirmed) {

    return;

}

try {

    const response =
        await fetch(
            `${API_BASE}/expenses/${id}`,
            {
                method: "DELETE"
            }
        );

    if (!response.ok) {

        const errorText =
            await response.text();

        throw new Error(
            errorText
        );

    }

    showMessage(
        "Expense deleted successfully.",
        "success"
    );

    // If deleted item was being edited
    if (
        editingExpenseId ===
        Number(id)
    ) {

        resetForm();

    }

    await loadExpenses();

} catch (error) {

    console.error(
        "Delete error:",
        error
    );

    showMessage(
        "Unable to delete the expense.",
        "error"
    );

}

}

// ============================================================
// RESET FORM
// ============================================================

function resetForm() {

editingExpenseId =
    null;

expenseForm.reset();

formDate.value =
    expenseDate.value;

formTitle.textContent =
    "Add Expense";

formDescription.textContent =
    "Add a new expense for the selected date.";

submitButton.textContent =
    "+ Add Expense";

cancelEditBtn.classList.add(
    "hidden"
);

addExpenseCard.classList.remove(
    "editing-mode"
);

}

// ============================================================
// CANCEL EDIT
// ============================================================

function cancelEdit() {

resetForm();

}

// ============================================================
// DATE CHANGE
// ============================================================

expenseDate.addEventListener(
"change",
() => {

    formDate.value =
        expenseDate.value;

    // If user changes date while
    // editing, cancel edit mode.

    if (
        editingExpenseId !== null
    ) {

        resetForm();

    }

}

);

// ============================================================
// LOAD BUTTON
// ============================================================

loadBtn.addEventListener(
"click",
loadExpenses
);

// ============================================================
// REFRESH BUTTON
// ============================================================

refreshBtn.addEventListener(
"click",
loadExpenses
);

// ============================================================
// FORM SUBMIT
// ============================================================

expenseForm.addEventListener(
"submit",
submitExpense
);

// ============================================================
// CANCEL EDIT BUTTON
// ============================================================

cancelEditBtn.addEventListener(
"click",
cancelEdit
);

// ============================================================
// FORM RESET BUTTON
// ============================================================

expenseForm.addEventListener(
"reset",
() => {

    setTimeout(
        () => {

            if (
                editingExpenseId !== null
            ) {

                resetForm();

            }

        },
        0
    );

}

);