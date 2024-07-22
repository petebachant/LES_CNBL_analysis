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
The code to produce all figures is in the folder `/paper_figures'

Calculate farm-averaged wake growth rate (change `path' variable on line 23! Some changes to code is required if you are using the KU Leuven public dataset)
```
calculate_wake_width.py
```
Calculate farm loss factors (change `path' variable on line 23! Some changes to code is required if you are using the KU Leuven public dataset)
```
calculate_farm_loss_factors.py
```
Predict farm-scale loss factors for wind farms (change `path' variable on line 23! Some changes to code is required if you are using the KU Leuven public dataset)
```
python predict_farm_scale_loss.py
```
