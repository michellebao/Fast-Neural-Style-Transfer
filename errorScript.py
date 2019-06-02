import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--groundtruth", type=str, required=True, dest="groundtruth",
 help="Directory path to batch of ground truth images")
parser.add_argument("--stylizedmodel", action="store", dest="stylizedmodel",
help="Directory path to batch of stylized images")
args = parser.parse_args()

def readPaths(groundtruth, model):
    groundtruthFrames = []
    modelFrames = []

    for i in [groundtruth, model]:
        sortedFiles = sorted(glob.glob(i + "/*.png"))
        for im_path in sortedFiles:
            im = imageio.imread(im_path)
            if i is groundtruth:
                groundtruthFrames.append(im)
            else:
                modelFrames.append(im)
    return groundtruthFrames, modelFrames

def temporalError(groundtruthFrames, modelFrames):
    H, W, C = groundtruthFrames[0].shape
    D = H * W * C
    T = len(groundtruthFrames)
    errorAvg = 0
    errorList = []
    eps = 0.01

    for img in range(T - 1):
        gtDiff = groundtruthFrames[img] - groundtruthFrames[img + 1]
        modelFrames_r1 = np.resize(modelFrames[img], (H, W, C))
        modelFrames_r2 = np.resize(modelFrames[img + 1], (H, W, C))
        modelDiff = modelFrames_r1 - modelFrames_r2

        frac = abs(np.square(gtDiff - modelDiff) / (gtDiff + eps)).mean()
        #frac = abs(np.square(baselineDiff - modelDiff)).mean()
        errorAvg += frac
        errorList.append(frac)
    errorAvg /= (T - 1)
    return errorAvg, errorList

def SSIM(groundtruthFrames, modelFrames):
    ssimTotal = 0;
    ssimList = []
    H, W, C = groundtruthFrames[0].shape
    for i in range(len(groundtruthFrames)):
        frame1 = groundtruthFrames[i]
        frame2 = modelFrames[i]
        frame2 = np.resize(frame2, (H, W, C))
        value = ssim(frame1, frame2, multichannel = True)
        ssimTotal += value
        ssimList.append(value)
    ssimAvg = ssimTotal / len(groundtruthFrames)
    return ssimAvg, ssimList

def

if __name__ == "__main__":
    groundtruthFrames, modelFrames = readPaths(args.groundtruth, args.stylizedmodel)
    errorAvg, errorList = temporalError(groundtruthFrames, modelFrames)
    ssimAvg, ssimList = SSIM(groundtruthFrames, modelFrames)
    print(groundtruthFrames)
    print(errorAvg)
    print(ssimAvg)
