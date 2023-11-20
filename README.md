# LES_CNBL_analysis
Clone github repository
```
git clone https://github.com/AndrewKirby2/LES_CNBL_analysis.git
```
Change directory
```
cd LES_CNBL_analysis
```
Create conda environment
```
conda env create -n LES_CNBL --file environment.yml
```
Load conda environment
```
conda activate LES_CNBL
```
Calculate turbine thrust coefficients and plot figures in plots/ folder (file paths for LES data need to be changed in this script!)
```
python calculate_thrust_coefficient.py
```
Calculate turbine power coefficients and plot figures in plots/ folder (file paths for LES data need to be changed in this script!)
```
python calculate_power_coefficient.py
```
