@echo off

REM Run all WDT output scripts from the project directory.
REM Helper modules (val_helpers, val_s_helpers, rates_s_helpers) are
REM excluded — they have no main() and are imported by the scripts below.

cd /d "%~dp0"

echo Current directory:
cd

for %%f in (
    "5_3_VAL_generate_appc_full.py"
    "5_4_VAL_generate_worked_examples.py"
    "5_6_VAL_generate_figures.py"
    "8_3_RATES_output.py"
    "16_2_VAL_S_rate_sweeps.py"
    "16_3_VAL_S_horizon_sweeps.py"
    "16_4_VAL_S_interactions.py"
    "16_5_VAL_S_assemble.py"
    "16_6_RATES_S_tables.py"
    "16_7_RATES_S_charts.py"
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