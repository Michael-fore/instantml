import torch
import torchvision.models as models
import torchvision.transforms as transform

class ImageHandle:
    '''TAkes care of img loading and sizing/transform. Most images will be b64 encoded 
     as they will be reciever from api'''
    def __init__(self):
        self.loader = transform.Compose([    
                                        transform.Resize((500,500)),
                                        transform.ToTensor(),
                                        transform.Normalize(mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225])])
    def load(self, img):
        self.img = self.loader(img).unsqueeze(0) #add dummy dim for 3d to 4d

class ImageModels(ImageHandle):
    '''Class prepares deep models for use, loads corrects answer sets, classifies.'''
    modes = {'AlexNet': models.alexnet(pretrained=True),
            'DenseNet': models.densenet161(pretrained=True),
            'GoogleNet': models.googlenet(pretrained=True),
            'Inception_V3': models.inception_v3(pretrained=True)
            }
    def __init__(self, mode):

        if mode not in modes.keys():
            raise KeyError('Needs to be AlexNet, DenseNet, GoogleNet, Inception_V3')
        
        self.net = self.modes.get(mode)

    def classify(self,  img):
        return self.net(img)