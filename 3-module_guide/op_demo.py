import copy
import torch
import torch.nn as nn
from torch.nn.parameter import Parameter
import torchvision

# n, cin, h, w, cout, kernel_size, stride, padding, dilation, eps
params = [
  [16, 32, 7, 7, 32, 3, 1, 1, 1, 1e-20]
]

def get_offset_mask(out, khmkw):
    offset = out[:,:2*khmkw]
    mask = out[:,2*khmkw:]
    mask = torch.sigmoid(mask)
    return offset, mask

def deform_conv2d_demo(n, cin, h, w, cout, kernel_size, stride, padding, dilation, eps):
  input_cpu = torch.randn(params[0][:4])
  conv_cpu = nn.Conv2d(cin, cout, kernel_size=kernel_size, stride=stride, padding=padding, bias=False)
  conv_output_cpu = conv_cpu(input_cpu)

  conv_output_cpu.retain_grad()
  dc_m_cpu = torchvision.ops.DeformConv2d(cin, cout, kernel_size, stride, padding, dilation, groups=1, bias=False)

  conv_offset = nn.Conv2d(cin, 3 * kernel_size * kernel_size,
                          kernel_size=kernel_size,
                          stride=stride,
                          padding=padding,
                          bias=False)

  offset_mask_cpu = conv_offset(input_cpu)
  offset_cpu, mask_cpu = get_offset_mask(offset_mask_cpu, kernel_size * kernel_size)
  dc_m_out_cpu = dc_m_cpu(conv_output_cpu, offset_cpu, mask_cpu)

  print(f"========input_cpu shape: {input_cpu.shape}")
  print(f"========conv_output_cpu: shape {conv_output_cpu.shape}")
  print(f"========offset_mask_cpu: shape {offset_mask_cpu.shape}")
  print(f"========offset_cpu shape: {offset_cpu.shape}")
  print(f"========mask_cpu shape: {mask_cpu.shape}")
  print(f"===========dc_m_out_cpu: {dc_m_out_cpu.shape}")


def transposed_conv_demo():
  in_channels = 16
  out_channels = 32
  kernel_size = 3
  stride = 2
  padding = 1

  # 创建转置卷积层
  trans_conv = nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, padding)

  # 生成一个随机输入张量
  batch_size = 1
  input_height = 8
  input_width = 8
  input_channels = in_channels
  input = torch.randn(batch_size, input_channels, input_height, input_width)

  # 进行转置卷积操作
  output = trans_conv(input)

  # 打印输出张量的形状
  print(output.shape)

def group_conv_demo():
  # 定义分组卷积的参数
  in_channels = 16
  out_channels = 32
  kernel_size = 3
  stride = 1
  padding = 1
  groups = 4

  # 创建分组卷积层
  group_conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, groups=groups)
  # weight_shape = (groups)

  print("groups shape: ", groups)
  print("output channels: ", out_channels)

  # 生成一个随机输入张量
  batch_size = 1
  input_height = 8
  input_width = 8
  input_channels = in_channels
  input = torch.randn(batch_size, input_channels, input_height, input_width)
  print("input shape: ", input.shape)

  # 进行分组卷积操作
  output = group_conv(input)

  # 打印输出张量的形状
  print("output shape: ", output.shape)

class LayerNorm(nn.Module):
    def __init__(self, d_model, eps=1e-12):
        super(LayerNorm, self).__init__()
        self.gamma = nn.Parameter(torch.ones(d_model))
        self.beta = nn.Parameter(torch.zeros(d_model))
        self.eps = eps

    def forward(self, x):
        mean = x.mean(-1, keepdim=True)
        var = x.var(-1, unbiased=False, keepdim=True)
        # '-1' means last dimension.

        out = (x - mean) / torch.sqrt(var + self.eps)
        out = self.gamma * out + self.beta
        return out

def batch_morm_demo():
  num_features = 16
  eps = 1e-5
  momentum = 0.1

  # 创建批归一化层
  batch_norm = nn.BatchNorm2d(num_features, eps=eps, momentum=momentum)
  # 定义层归一化的参数
  normalized_shape = [16, 8, 8]

  # 创建层归一化层
  layer_norm = nn.LayerNorm(normalized_shape)

  # 生成一个随机输入张量
  batch_size = 1
  input_height = 8
  input_width = 8
  input_channels = num_features
  input = torch.randn(batch_size, input_channels, input_height, input_width)

  # 进行批归一化操作
  batch_norm_output = batch_norm(input)

  # 进行层归一化操作
  layer_norm_output = layer_norm(input)


if __name__ == "__main__":
  # deform_conv2d_demo(*params[0])
  # transposed_conv_demo()
  group_conv_demo()
  print("run op_demo.py successfully !!!")