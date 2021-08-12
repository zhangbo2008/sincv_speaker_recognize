import torch.nn.functional as F
import torch
waveforms=torch.tensor([[[1,2,4]]])
filters=torch.tensor([[[2,4,5]]])


b=F.conv1d(waveforms, filters, stride=1,
                        groups=1)  # 窗口大小251,每一次步长是1.输出特征维度是80.
print(1)