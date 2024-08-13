from omrdatasettools import Downloader, OmrDataset

Downloader().download_and_extract_dataset(
    dataset=OmrDataset.Rebelo2, 
    destination_directory="D:\PY_PROGS\AIGenerationMusic.github.io\dataset",
)