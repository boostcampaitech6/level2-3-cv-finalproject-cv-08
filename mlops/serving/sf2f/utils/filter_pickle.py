import pickle
import os


def check_pickle(mel_pickle):
    """
    Load a mel pickle file and remove the file if it is empty

    Args:
        mel_pickle: str, path to the mel pickle file
    Returns:
        None
    """
    file = open(mel_pickle, 'rb')
    try:
        data = pickle.load(file)
    except:
        print('Error loading:', mel_pickle)
        os.remove(mel_pickle)
        
    file.close()

def filtering_pickle(dir_path):
    for dir in os.listdir(dir_path):
        data_path = os.path.join(dir_path, dir)
        for id in os.listdir(data_path):
            data = os.path.join(data_path, id)
            check_pickle(data)
    print("Filtering Done.")


# if __name__=="__main__":
#     dir_path = './data/VoxCeleb/vox1/mel_spectrograms' # wav_convertor.vox1_mel
#     filtering_pickle(dir_path)

