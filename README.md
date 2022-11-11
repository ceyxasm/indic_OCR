

## Updates
* **Nov 11, 2022**: starting 10-nov-2022 all updates will be reflected [here](https://ceyxasm.github.io/auto_grader/)
* **Nov 8, 2022**: init 

## Getting Started
### Dependency
- Tested with PyTorch 1.3.1, CUDA 10.1, python 3.6 and Ubuntu 16.04. <br>`pip3 install torch==1.3.1`. <br>
- requirements : lmdb, pillow, torchvision, nltk, natsort <br>
`
pip3 install lmdb pillow torchvision nltk natsort
`

### Download dataset for traininig and evaluation from [here](http://cvit.iiit.ac.in/ihtr2022/dataset.html)
* [training data](http://cvit.iiit.ac.in/ihtr2022/assets/dataset/trainingset.zip)
* [validation data](http://cvit.iiit.ac.in/ihtr2022/assets/dataset/validationset.zip)
* [test data](http://cvit.iiit.ac.in/ihtr2022/assets/dataset/testset.zip)
Each data.zip contains 10 subfolders. 1 for each language (bengali  devanagari  gujarati  gurumukhi  kannada  malayalam  odia  tamil  telugu  urdu). <br>


### Run demo with pretrained model
1. Download pretrained model from [here](pretrained_models/hindi_10e5_iter.pth)
  * The model is trained on Devnagri
  * training details can be found [here](dev_10e5_results/opt.txt)
2. Add image files to test into `demo_image/`
3. Run demo.py (add `--sensitive` option if you use case-sensitive model)
```
CUDA_VISIBLE_DEVICES=0 python3 demo.py \
--Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn \
--image_folder demo_image/ \
--saved_model <path_to_the_saved_model>
```


### Training and evaluation
1. Train CRNN[10] model
```
CUDA_VISIBLE_DEVICES=0 python3 train.py \
--train_data data_lmdb_release/training --valid_data data_lmdb_release/validation \
--select_data 1 --batch_ratio / \
--Transformation None --FeatureExtraction VGG --SequenceModeling BiLSTM --Prediction CTC
```
2. Test CRNN[10] model.  
```
CUDA_VISIBLE_DEVICES=0 python3 test.py \
--eval_data data_lmdb_release/evaluation --benchmark_all_eval \
--Transformation None --FeatureExtraction VGG --SequenceModeling BiLSTM --Prediction CTC \
--saved_model saved_models/None-VGG-BiLSTM-CTC-Seed1111/best_accuracy.pth
```

### Arguments
* `--train_data`: folder path to training lmdb dataset.
* `--valid_data`: folder path to validation lmdb dataset.
* `--select_data`: select training data. default is MJ-ST, which means MJ and ST used as training data.
* `--batch_ratio`: assign ratio for each selected data in the batch. 
* `--data_filtering_off`: skip data filtering when creating LmdbDataset. 
* `--Transformation`: select Transformation module [None | TPS].
* `--FeatureExtraction`: select FeatureExtraction module [VGG | RCNN | ResNet].
* `--SequenceModeling`: select SequenceModeling module [None | BiLSTM].
* `--Prediction`: select Prediction module [CTC | Attn].
* `--saved_model`: assign saved model to evaluation.

## When you need to train on your own language datasets.
1. Create your own lmdb dataset.
```
pip3 install fire
python3 create_lmdb_dataset.py --inputPath data/ --gtFile data/gt.txt --outputPath result/
```
The structure of data folder as below. Refer for ICFHR dataset structure for better understanding.
```
data
├── gt.txt
└── test
    ├── word_1.png
    ├── word_2.png
    ├── word_3.png
    └── ...
```
At this time, `gt.txt` should be `{imagepath}\t{label}\n` <br>
For example
```
test/word_1.png Tiredness
test/word_2.png kills
test/word_3.png A
...
```
2. Modify `--select_data`, `--batch_ratio`, and `opt.character`.
3. This procedure needs to be repeated for each single training and validation folder, for each language in [ICFHR_dataset](http://cvit.iiit.ac.in/ihtr2022/dataset.html)


