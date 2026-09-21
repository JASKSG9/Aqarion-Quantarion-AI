"use strict";

/*
AQARION Smith Normal Form Quotient Dashboard

Matrix convention:
A is m × n, representing the integer homomorphism

A : Z^n → Z^m.

The quotient group is:

coker(A) = Z^m / im(A).

If the Smith normal form has nonzero diagonal entries:

d1, ..., dk,

with d_i > 0 and d_i | d_(i+1), then:

coker(A) ≅ Z^(m-k) ⊕ ⨁_(d_i > 1) Z/d_i Z.

All arithmetic uses BigInt. The interactive UI is intended for educational and
moderate-size matrices, with row count capped at 10 and column count capped at 12.
*/

const state = {
  rows: 2,
  columns: 1,
  latestResult: null,
};

const rowCountInput = document.getElementById("rowCount");
const columnCountInput = document.getElementById("columnCount");
const resizeMatrixButton = document.getElementById("resizeMatrixButton");
const computeButton = document.getElementById("computeButton");
const clearMatrixButton = document.getElementById("clearMatrixButton");
const matrixEditor = document.getElementById("matrixEditor");
const matrixShape = document.getElementById("matrixShape");

const decompositionResult = document.getElementById("decompositionResult");
const projectionResult = document.getElementById("projectionResult");
const invariantResult = document.getElementById("invariantResult");
const projectionVisualization = document.getElementById("projectionVisualization");
const relationMatrixDisplay = document.getElementById("relationMatrixDisplay");
const smithMatrixDisplay = document.getElementById("smithMatrixDisplay");

const tooltip = document.getElementById("tooltip");

/* ---------- Exact integer helpers ---------- */

function absBigInt(value) {
  return value < 0n ? -value : value;
}

function gcdBigInt(a, b) {
  a = absBigInt(a);
  b = absBigInt(b);

  while (b !== 0n) {
    [a, b] = [b, a % b];
  }

  return a;
}

function parseStrictInteger(value, label) {
  const text = String(value).trim();

  if (!/^-?d+$/.test(text)) {
    throw new Error(`${label} must be an integer.`);
  }

  return BigInt(text);
}

function parseBoundedInteger(value, label, min, max) {
  const parsed = Number(parseStrictInteger(value, label));

  if (!Number.isSafeInteger(parsed) || parsed < min || parsed > max) {
    throw new Error(`${label} must be an integer from ${min} to ${max}.`);
  }

  return parsed;
}

function cloneMatrix(matrix) {
  return matrix.map((row) => row.slice());
}

function zeroMatrix(rows, columns) {
  return Array.from(
    { length: rows },
    () => Array.from({ length: columns }, () => 0n),
  );
}

/* ---------- Rational rank calculation ---------- */

function normalizeFraction(fraction) {
  if (fraction.numerator === 0n) {
    return { numerator: 0n, denominator: 1n };
  }

  const divisor = gcdBigInt(
    fraction.numerator,
    fraction.denominator,
  );

  let numerator = fraction.numerator / divisor;
  let denominator = fraction.denominator / divisor;

  if (denominator < 0n) {
    numerator = -numerator;
    denominator = -denominator;
  }

  return { numerator, denominator };
}

function multiplyFraction(left, right) {
  return normalizeFraction({
    numerator: left.numerator * right.numerator,
    denominator: left.denominator * right.denominator,
  });
}

function subtractFraction(left, right) {
  return normalizeFraction({
    numerator:
      left.numerator * right.denominator
      - right.numerator * left.denominator,
    denominator: left.denominator * right.denominator,
  });
}

function divideFraction(left, right) {
  if (right.numerator === 0n) {
    throw new Error("Internal rational-rank division by zero.");
  }

  return normalizeFraction({
    numerator: left.numerator * right.denominator,
    denominator: left.denominator * right.numerator,
  });
}

function matrixRankOverQ(inputMatrix) {
  if (inputMatrix.length === 0) {
    return 0;
  }

  if (inputMatrix[0].length === 0) {
    return 0;
  }

  const matrix = inputMatrix.map((row) =>
    row.map((entry) => ({
      numerator: entry,
      denominator: 1n,
    })),
  );

  const rows = matrix.length;
  const columns = matrix[0].length;
  let rank = 0;
  let pivotRow = 0;

  for (
    let pivotColumn = 0;
    pivotColumn < columns && pivotRow < rows;
    pivotColumn += 1
  ) {
    let candidateRow = pivotRow;

    while (
      candidateRow < rows
      && matrix[candidateRow][pivotColumn].numerator === 0n
    ) {
      candidateRow += 1;
    }

    if (candidateRow === rows) {
      continue;
    }

    [matrix[pivotRow], matrix[candidateRow]] =
      [matrix[candidateRow], matrix[pivotRow]];

    const pivot = matrix[pivotRow][pivotColumn];

    for (let column = pivotColumn; column < columns; column += 1) {
      matrix[pivotRow][column] = divideFraction(
        matrix[pivotRow][column],
        pivot,
      );
    }

    for (let row = 0; row < rows; row += 1) {
      if (row === pivotRow) {
        continue;
      }

      const coefficient = matrix[row][pivotColumn];

      if (coefficient.numerator === 0n) {
        continue;
      }

      for (let column = pivotColumn; column < columns; column += 1) {
        matrix[row][column] = subtractFraction(
          matrix[row][column],
          multiplyFraction(coefficient, matrix[pivotRow][column]),
        );
      }
    }

    pivotRow += 1;
    rank += 1;
  }

  return rank;
}

/* ---------- Smith normal form operations ---------- */

function swapRows(matrix, firstRow, secondRow) {
  [matrix[firstRow], matrix[secondRow]] =
    [matrix[secondRow], matrix[firstRow]];
}

function swapColumns(matrix, firstColumn, secondColumn) {
  for (const row of matrix) {
    [row[firstColumn], row[secondColumn]] =
      [row[secondColumn], row[firstColumn]];
  }
}

function multiplyRow(matrix, rowIndex, scalar) {
  for (let column = 0; column < matrix[rowIndex].length; column += 1) {
    matrix[rowIndex][column] *= scalar;
  }
}

function addRowMultiple(matrix, targetRow, sourceRow, multiple) {
  for (let column = 0; column < matrix[targetRow].length; column += 1) {
    matrix[targetRow][column] += multiple * matrix[sourceRow][column];
  }
}

function addColumnMultiple(matrix, targetColumn, sourceColumn, multiple) {
  for (let row = 0; row < matrix.length; row += 1) {
    matrix[row][targetColumn] += multiple * matrix[row][sourceColumn];
  }
}

function findSmallestNonzero(matrix, startIndex) {
  let candidate = null;

  for (let row = startIndex; row < matrix.length; row += 1) {
    for (
      let column = startIndex;
      column < matrix[0].length;
      column += 1
    ) {
      const value = matrix[row][column];

      if (value === 0n) {
        continue;
      }

      if (
        candidate === null
        || absBigInt(value) < absBigInt(candidate.value)
      ) {
        candidate = { row, column, value };
      }
    }
  }

  return candidate;
}

function findEntryNotDivisibleByPivot(matrix, startIndex, pivot) {
  for (let row = startIndex; row < matrix.length; row += 1) {
    for (
      let column = startIndex;
      column < matrix[0].length;
      column += 1
    ) {
      if (matrix[row][column] % pivot !== 0n) {
        return { row, column };
      }
    }
  }

  return null;
}

function smithNormalFormDiagonal(inputMatrix) {
  if (inputMatrix.length === 0 || inputMatrix[0].length === 0) {
    return [];
  }

  const matrix = cloneMatrix(inputMatrix);
  const rowCount = matrix.length;
  const columnCount = matrix[0].length;
  const diagonal = [];

  let index = 0;

  while (index < rowCount && index < columnCount) {
    let smallest = findSmallestNonzero(matrix, index);

    if (smallest === null) {
      break;
    }

    swapRows(matrix, index, smallest.row);
    swapColumns(matrix, index, smallest.column);

    let pivotSettled = false;

    while (!pivotSettled) {
      pivotSettled = true;

      /*
      Euclidean reduction down the current pivot column.
      */
      for (let row = index + 1; row < rowCount; row += 1) {
        if (matrix[row][index] === 0n) {
          continue;
        }

        const pivot = matrix[index][index];
        const quotient = matrix[row][index] / pivot;

        addRowMultiple(matrix, row, index, -quotient);

        if (
          matrix[row][index] !== 0n
          && absBigInt(matrix[row][index])
            < absBigInt(matrix[index][index])
        ) {
          swapRows(matrix, row, index);
        }

        pivotSettled = false;
      }

      /*
      Euclidean reduction across the current pivot row.
      */
      for (
        let column = index + 1;
        column < columnCount;
        column += 1
      ) {
        if (matrix[index][column] === 0n) {
          continue;
        }

        const pivot = matrix[index][index];
        const quotient = matrix[index][column] / pivot;

        addColumnMultiple(matrix, column, index, -quotient);

        if (
          matrix[index][column] !== 0n
          && absBigInt(matrix[index][column])
            < absBigInt(matrix[index][index])
        ) {
          swapColumns(matrix, column, index);
        }

        pivotSettled = false;
      }

      if (matrix[index][index] === 0n) {
        smallest = findSmallestNonzero(matrix, index);

        if (smallest === null) {
          break;
        }

        swapRows(matrix, index, smallest.row);
        swapColumns(matrix, index, smallest.column);
        pivotSettled = false;
        continue;
      }

      if (!pivotSettled) {
        continue;
      }

      const pivot = matrix[index][index];
      const nonDivisible = findEntryNotDivisibleByPivot(
        matrix,
        index + 1,
        pivot,
      );

      if (nonDivisible !== null) {
        /*
        Introduce this entry into the pivot row, then repeat Euclidean
        reduction until the pivot divides every entry in the trailing block.
        */
        addRowMultiple(matrix, index, nonDivisible.row, 1n);

        if (matrix[index][index] === 0n) {
          swapColumns(matrix, index, nonDivisible.column);
        }

        pivotSettled = false;
      }
    }

    if (matrix[index][index] === 0n) {
      break;
    }

    if (matrix[index][index] < 0n) {
      multiplyRow(matrix, index, -1n);
    }

    const pivot = matrix[index][index];

    for (let row = index + 1; row < rowCount; row += 1) {
      if (matrix[row][index] !== 0n) {
        addRowMultiple(
          matrix,
          row,
          index,
          -(matrix[row][index] / pivot),
        );
      }
    }

    for (
      let column = index + 1;
      column < columnCount;
      column += 1
    ) {
      if (matrix[index][column] !== 0n) {
        addColumnMultiple(
          matrix,
          column,
          index,
          -(matrix[index][column] / pivot),
        );
      }
    }

    diagonal.push(absBigInt(matrix[index][index]));
    index += 1;
  }

  return diagonal.filter((entry) => entry !== 0n);
}

/* ---------- Matrix editor ---------- */

function matrixInputId(row, column) {
  return `matrix-entry-${row}-${column}`;
}

function getCurrentEditorValues() {
  const values = [];

  for (let row = 0; row < state.rows; row += 1) {
    const currentRow = [];

    for (let column = 0; column < state.columns; column += 1) {
      const input = document.getElementById(matrixInputId(row, column));
      currentRow.push(input ? input.value : "0");
    }

    values.push(currentRow);
  }

  return values;
}

function renderMatrixEditor(existingValues = null) {
  matrixEditor.innerHTML = "";
  matrixEditor.style.setProperty(
    "--matrix-columns",
    String(Math.max(state.columns, 1)),
  );

  matrixShape.textContent = `${state.rows} × ${state.columns}`;

  if (state.columns === 0) {
    matrixEditor.innerHTML = `
      <div class="empty-result">
        No relation columns. The quotient is the free group ℤ^${state.rows}.
      </div>
    `;
    return;
  }

  for (let row = 0; row < state.rows; row += 1) {
    for (let column = 0; column < state.columns; column += 1) {
      const input = document.createElement("input");
      input.className = "matrix-entry";
      input.type = "text";
      input.inputMode = "numeric";
      input.value = (
        existingValues
        && existingValues[row]
        && existingValues[row][column] !== undefined
      )
        ? existingValues[row][column]
        : "0";

      input.id = matrixInputId(row, column);
      input.setAttribute(
        "aria-label",
        `Matrix entry row ${row + 1}, column ${column + 1}`,
      );

      matrixEditor.appendChild(input);
    }
  }
}

function resizeMatrix() {
  try {
    const existingValues = getCurrentEditorValues();

    state.rows = parseBoundedInteger(
      rowCountInput.value,
      "Ambient generators m",
      1,
      10,
    );

    state.columns = parseBoundedInteger(
      columnCountInput.value,
      "Relation columns n",
      0,
      12,
    );

    rowCountInput.value = String(state.rows);
    columnCountInput.value = String(state.columns);

    renderMatrixEditor(existingValues);
  } catch (error) {
    showError(error.message);
  }
}

function clearMatrix() {
  renderMatrixEditor();
  clearRenderedResults();
}

/* ---------- Computation ---------- */

function readMatrix() {
  if (state.columns === 0) {
    return zeroMatrix(state.rows, 0);
  }

  const matrix = zeroMatrix(state.rows, state.columns);

  for (let row = 0; row < state.rows; row += 1) {
    for (let column = 0; column < state.columns; column += 1) {
      const input = document.getElementById(matrixInputId(row, column));

      matrix[row][column] = parseStrictInteger(
        input.value,
        `Entry A[${row + 1},${column + 1}]`,
      );
    }
  }

  return matrix;
}

function factorDivisibilityCheck(diagonal) {
  for (let index = 0; index + 1 < diagonal.length; index += 1) {
    if (diagonal[index + 1] % diagonal[index] !== 0n) {
      return false;
    }
  }

  return true;
}

function computeQuotientStructure(matrix) {
  const rows = matrix.length;
  const columns = matrix[0] ? matrix[0].length : 0;
  const diagonal = columns === 0
    ? []
    : smithNormalFormDiagonal(matrix);

  const rationalRank = matrixRankOverQ(matrix);
  const freeRank = rows - rationalRank;
  const torsionFactors = diagonal.filter((value) => value > 1n);
  const finite = freeRank === 0;
  const order = finite
    ? torsionFactors.reduce((product, factor) => product * factor, 1n)
    : null;

  if (!factorDivisibilityCheck(diagonal)) {
    throw new Error(
      "Internal Smith-normal-form consistency check failed: diagonal factors are not ordered by divisibility.",
    );
  }

  return {
    matrix,
    rows,
    columns,
    diagonal,
    rank: rationalRank,
    freeRank,
    torsionFactors,
    finite,
    order,
    cyclic: (
      (freeRank === 0 && torsionFactors.length <= 1)
      || (freeRank === 1 && torsionFactors.length === 0)
    ),
  };
}

function runComputation() {
  try {
    const matrix = readMatrix();
    const result = computeQuotientStructure(matrix);
    state.latestResult = result;
    renderResults(result);
  } catch (error) {
    showError(error.message);
  }
}

/* ---------- Result display ---------- */

function formatBigInt(value) {
  return value.toString();
}

function groupStructure(result) {
  const factors = [];

  if (result.freeRank === 1) {
    factors.push("ℤ");
  } else if (result.freeRank > 1) {
    factors.push(`ℤ^${result.freeRank}`);
  }

  for (const torsionFactor of result.torsionFactors) {
    factors.push(`ℤ/${formatBigInt(torsionFactor)}ℤ`);
  }

  return factors.length > 0 ? factors.join(" ⊕ ") : "0";
}

function matrixToText(matrix) {
  if (matrix.length === 0) {
    return "[]";
  }

  if (matrix[0].length === 0) {
    return matrix.map(() => "[]").join("
");
  }

  const stringRows = matrix.map((row) =>
    row.map((entry) => formatBigInt(entry)),
  );

  const widths = Array.from(
    { length: stringRows[0].length },
    (_, column) => Math.max(
      ...stringRows.map((row) => row[column].length),
    ),
  );

  return stringRows
    .map((row) =>
      `[ ${row.map(
        (entry, column) => entry.padStart(widths[column], " "),
      ).join("  ")} ]`,
    )
    .join("
");
}

function diagonalMatrixToText(rows, columns, diagonal) {
  if (columns === 0) {
    return Array.from({ length: rows }, () => "[]").join("
");
  }

  const matrix = zeroMatrix(rows, columns);

  diagonal.forEach((entry, index) => {
    matrix[index][index] = entry;
  });

  return matrixToText(matrix);
}

function renderResults(result) {
  const structure = groupStructure(result);

  decompositionResult.className = "decomposition-display";
  decompositionResult.innerHTML = `
    <div class="structure-main">
      coker(A) ≅ ${escapeHtml(structure)}
    </div>

    <ul class="result-list">
      <li>
        <span class="result-key">Presentation</span>
        <span class="result-value">ℤ^${result.rows} / im(A)</span>
      </li>
      <li>
        <span class="result-key">Matrix rank</span>
        <span class="result-value">${result.rank}</span>
      </li>
      <li>
        <span class="result-key">Free rank</span>
        <span class="result-value">${result.freeRank}</span>
      </li>
      <li>
        <span class="result-key">Nontrivial torsion</span>
        <span class="result-value">${
          result.torsionFactors.length === 0
            ? "none"
            : result.torsionFactors
              .map((factor) => `ℤ/${formatBigInt(factor)}ℤ`)
              .join(" ⊕ ")
        }</span>
      </li>
      <li>
        <span class="result-key">Finite quotient</span>
        <span class="result-value">${
          result.finite ? "yes" : "no"
        }</span>
      </li>
      <li>
        <span class="result-key">Quotient order</span>
        <span class="result-value">${
          result.finite ? formatBigInt(result.order) : "infinite"
        }</span>
      </li>
    </ul>
  `;

  projectionResult.innerHTML = `
    <ul class="result-list">
      <li>
        <span class="result-key">Ambient free group</span>
        <span class="result-value">ℤ^${result.rows}</span>
      </li>
      <li>
        <span class="result-key">Relation subgroup</span>
        <span class="result-value">im(A)</span>
      </li>
      <li>
        <span class="result-key">Projection</span>
        <span class="result-value">π(x) = x + im(A)</span>
      </li>
      <li>
        <span class="result-key">Kernel</span>
        <span class="result-value">ker(π) = im(A)</span>
      </li>
      <li>
        <span class="result-key">Identity image</span>
        <span class="result-value">π(0) = im(A)</span>
      </li>
      <li>
        <span class="result-key">Projection property</span>
        <span class="result-value">surjective homomorphism</span>
      </li>
    </ul>
  `;

  invariantResult.innerHTML = `
    <ul class="result-list">
      <li>
        <span class="result-key">SNF nonzero pivots</span>
        <span class="result-value">${
          result.diagonal.length === 0
            ? "none"
            : result.diagonal.map(formatBigInt).join(", ")
        }</span>
      </li>
      <li>
        <span class="result-key">Divisibility chain</span>
        <span class="result-value status-pass">dᵢ divides dᵢ₊₁</span>
      </li>
      <li>
        <span class="result-key">Trivial factors removed</span>
        <span class="result-value">${
          result.diagonal.filter((value) => value === 1n).length
        }</span>
      </li>
      <li>
        <span class="result-key">Cyclic quotient</span>
        <span class="result-value">${
          result.cyclic ? "yes" : "no"
        }</span>
      </li>
      <li>
        <span class="result-key">Finite / infinite</span>
        <span class="result-value">${
          result.finite ? "finite" : "infinite"
        }</span>
      </li>
    </ul>
  `;

  relationMatrixDisplay.textContent = matrixToText(result.matrix);
  smithMatrixDisplay.textContent = diagonalMatrixToText(
    result.rows,
    result.columns,
    result.diagonal,
  );

  renderProjectionVisualization(result);
}

function renderProjectionVisualization(result) {
  const torsionChips = result.torsionFactors
    .slice(0, 10)
    .map((factor, index) => (
      `<span class="coset-chip">torsion ${index + 1}: ℤ/${formatBigInt(factor)}ℤ</span>`
    ));

  if (result.torsionFactors.length > 10) {
    torsionChips.push(
      `<span class="coset-chip warning">+ ${
        result.torsionFactors.length - 10
      } additional torsion factors</span>`,
    );
  }

  if (result.freeRank > 0) {
    torsionChips.unshift(
      `<span class="coset-chip warning">free part: ℤ^${result.freeRank}</span>`,
    );
  }

  if (torsionChips.length === 0) {
    torsionChips.push(
      `<span class="coset-chip">trivial quotient</span>`,
    );
  }

  projectionVisualization.innerHTML = `
    <div class="projection-flow">
      <div class="visual-box">
        <h3>Ambient lattice</h3>
        <p class="math">ℤ^${result.rows}</p>
        <p>
          The ${result.columns} column${
            result.columns === 1 ? "" : "s"
          } of <span class="math">A</span> generate
          <span class="math">im(A)</span>.
        </p>
        <p>
          Vectors differing by an element of
          <span class="math">im(A)</span> become the same quotient class.
        </p>
      </div>

      <div class="projection-arrow" aria-label="canonical projection">⟶</div>

      <div class="visual-box">
        <h3>Quotient classes</h3>
        <p class="math">π(x)=x+im(A)</p>
        <p class="math">coker(A) ≅ ${escapeHtml(groupStructure(result))}</p>
        <div class="coset-chip-grid">
          ${torsionChips.join("")}
        </div>
      </div>
    </div>
  `;
}

function clearRenderedResults() {
  decompositionResult.className = "empty-result";
  decompositionResult.textContent =
    "Enter a matrix and choose “Compute Smith normal form.”";

  projectionResult.className = "empty-result";
  projectionResult.textContent = "No matrix has been computed.";

  invariantResult.className = "empty-result";
  invariantResult.textContent = "No matrix has been computed.";

  projectionVisualization.innerHTML = `
    <div class="empty-result">
      Compute a matrix to visualize the quotient projection.
    </div>
  `;

  relationMatrixDisplay.textContent = "—";
  smithMatrixDisplay.textContent = "—";
}

function showError(message) {
  decompositionResult.className = "empty-result";
  decompositionResult.innerHTML = `
    <span class="status-fail">Input or computation error:</span>
    ${escapeHtml(message)}
  `;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

/* ---------- Presets ---------- */

const presets = {
  cyclic: {
    rows: 1,
    columns: 2,
    matrix: [["12", "4"]],
  },

  diagonal: {
    rows: 2,
    columns: 2,
    matrix: [
      ["4", "0"],
      ["0", "12"],
    ],
  },

  freeTorsion: {
    rows: 2,
    columns: 1,
    matrix: [
      ["0"],
      ["6"],
    ],
  },

  zero: {
    rows: 2,
    columns: 0,
    matrix: [
      [],
      [],
    ],
  },

  nonCyclic: {
    rows: 2,
    columns: 2,
    matrix: [
      ["2", "0"],
      ["0", "2"],
    ],
  },
};

function loadPreset(name) {
  const preset = presets[name];

  if (!preset) {
    return;
  }

  state.rows = preset.rows;
  state.columns = preset.columns;

  rowCountInput.value = String(preset.rows);
  columnCountInput.value = String(preset.columns);

  renderMatrixEditor(preset.matrix);
  runComputation();
}

/* ---------- Tooltip behavior ---------- */

function initializeTooltips() {
  document.querySelectorAll("[data-tooltip]").forEach((button) => {
    const show = () => {
      tooltip.textContent = button.dataset.tooltip.trim();
      tooltip.classList.remove("hidden");

      const buttonRect = button.getBoundingClientRect();
      const width = Math.min(330, window.innerWidth - 28);

      let left = buttonRect.left;
      let top = buttonRect.bottom + 10;

      if (left + width > window.innerWidth - 14) {
        left = window.innerWidth - width - 14;
      }

      if (top + 170 > window.innerHeight) {
        top = Math.max(14, buttonRect.top - 180);
      }

      tooltip.style.left = `${Math.max(14, left)}px`;
      tooltip.style.top = `${top}px`;
    };

    const hide = () => tooltip.classList.add("hidden");

    button.addEventListener("mouseenter", show);
    button.addEventListener("mouseleave", hide);
    button.addEventListener("focus", show);
    button.addEventListener("blur", hide);
  });
}

/* ---------- Events and initialization ---------- */

resizeMatrixButton.addEventListener("click", resizeMatrix);
computeButton.addEventListener("click", runComputation);
clearMatrixButton.addEventListener("click", clearMatrix);

document.querySelectorAll("[data-preset]").forEach((button) => {
  button.addEventListener("click", () => {
    loadPreset(button.dataset.preset);
  });
});

renderMatrixEditor([["12"], ["0"]]);
loadPreset("cyclic");
initializeTooltips();
