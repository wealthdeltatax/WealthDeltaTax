@echo off

REM Run all WDT output scripts from the project directory.
REM Helper modules (val_helpers, val_s_helpers, rates_s_helpers) are
REM excluded — they have no main() and are imported by the scripts below.

cd /d "%~dp0"

echo Current directory:
cd

for %%f in (
    "val_core.py",
    "rates_core.py",
    "sweeeps_core.py",
    "wfr_core.py",
    "ldw_core.py",
    "5_3_VAL_tables.py",
    "5_4_VAL_charts.py",
    "5_5_VAL_generate_worked_examples.py",
    "8_2_RATES_tables.py",
    "8_3_RATES_charts.py",
    "16_1_SWEEPS_V_tables.py",
    "16_2_SWEEPS_V_charts.py",
    "16_3_SWEEPS_R_tables.py",
    "16_4_SWEEPS_R_charts.py",
    "19_2_WFR_tables.py",
    "19_3_WFR_charts.py"
) do (
    echo.
    echo ========================================
    echo Running %%f
    echo ========================================

    python %%f

    if errorlevel 1 (
        echo ERROR running %%f
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo All scripts completed successfully.
echo ========================================
pause