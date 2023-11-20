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
Calculate turbine thrust coefficients and plot figures in plots/ folder
```
python calculate_thrust_coefficient.py
```
Calculate turbine power coefficients and plot figures in plots/ folder
```
python calculate_power_coefficient.py
```
