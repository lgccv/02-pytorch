import torch
import numpy as np

def reqiregrad_set():
    xx = torch.tensor([1, 2, 4], dtype = torch.float, requires_grad=True)
    aa = np.array([1, 2, 3])
    yy = torch.from_numpy(aa).to(torch.float)
    yy.requires_grad = True
    print("tensor requires_grad: ", yy.requires_grad)

# 全连接层计算梯度 tiny
def autograd_demo():
    x = torch.ones(5)  # input tensor
    y = torch.zeros(3)  # expected output
    w = torch.randn(5, 3, requires_grad=True) # requires_grad
    b = torch.randn(3, requires_grad=True)    
    z = torch.matmul(x, w)+b # 全连接层
    
    loss = torch.nn.functional.binary_cross_entropy_with_logits(z, y)
    print(f"Gradient function for z = {z.grad_fn}")
    print(f"Gradient function for loss = {loss.grad_fn}")
    loss.backward() # 反向传播：求梯度
    print(w.grad)
    print(b.grad)
    print(y.grad) # 
    print(z.grad) # 中间结果不保存
    print("z requires_grad: ", z.requires_grad) #
    
def internal_grad_demo():
    x = torch.ones(5)  # input tensor
    y = torch.zeros(3)  # expected output
    w = torch.randn(5, 3, requires_grad=True) # requires_grad
    b = torch.randn(3, requires_grad=True)    
    z = torch.matmul(x, w)+b # 全连接层
    print("z shape: ", z.shape)
    output_grad = torch.randn_like(z)
    z.backward(output_grad)
    
def set_no_grad():
    x = torch.ones(5, requires_grad=True)  # input tensor
    y = torch.zeros(3)  # expected output
    w = torch.randn(5, 3, requires_grad=True) # requires_grad
    b = torch.randn(3, requires_grad=True) 
    z = torch.matmul(x, w)+b
    # print("requires_grad: ", z.requires_grad)
    z.backward(torch.randn_like(z))
    print("x grad: ", x.grad)
    
    # torch.set_grad_enabled(False) # 全局设置 requires_grad = False
    
    with torch.no_grad():
        z = torch.matmul(x, w)+b
    print("requires_grad: ", z.requires_grad)
    
def grad_sum():
    # torch.seed()
    x = torch.ones(5)  # input tensor
    label = torch.zeros(3)  # expected output
    w = torch.randn(5, 3, requires_grad=True) # requires_grad
    b = torch.randn(3, requires_grad=True)    
    output = torch.matmul(x, w)+b # 全连接层 
    
    loss = torch.nn.functional.binary_cross_entropy_with_logits(output, label)
    loss.backward(retain_graph=True) # 反向传播：求梯度
    print(f"Grad for w first time = {w.grad}")
    print(f"Gradient function for z = {output.grad_fn}")
    print(f"Gradient function for loss = {loss.grad_fn}")
    w.grad.zero_()
    loss.backward(retain_graph=True)
    print(f"Grad for w second time = {w.grad}")
    
    
def hook_demo():
    v = torch.tensor([0., 0., 0.], requires_grad=True)
    h = v.register_hook(lambda grad: grad * 1 + 2)  # double the gradient
    v.backward(torch.tensor([1., 2., 3.]))
    print("v grad: ", v.grad)
    
def get_inter_grad():
    z_grad = []
    # def get_grad(grad):
    #     z_grad.append(grad)
        
    torch.manual_seed(0)
    x = torch.ones(5)  # input tensor
    label = torch.zeros(3)  # expected output
    w = torch.randn(5, 3, requires_grad=True) # requires_grad
    b = torch.randn(3, requires_grad=True)    
    output = torch.matmul(x, w)+b # 全连接层
    output.retain_grad()
    # output.register_hook(get_grad)    
    loss = torch.nn.functional.binary_cross_entropy_with_logits(output, label)
    loss.backward(retain_graph=True) # 反向传播：求梯度
    print("output grad: ", output.grad)   
    
class Exp(torch.autograd.Function):
    @staticmethod
    def forward(ctx, i):
        result = i.exp()
        ctx.save_for_backward(result)
        return result

    @staticmethod
    def backward(ctx, grad_output):
        print("==============")
        result, = ctx.saved_tensors
        return grad_output * result
    
def custom_demo():
    input = torch.randn(5, 6)
    input.requires_grad=True
    output = Exp.apply(input)
    output.backward(torch.rand(5, 6))
    print("output: ", input)
    print("output grad: ", input.grad)
    
if __name__ == "__main__":
    # reqiregrad_set()
    # autograd_demo()
    # internal_grad_demo()
    # set_no_grad()
    # grad_sum()
    # hook_demo()
    # get_inter_grad()
    custom_demo()
    print("run autograd_demo.py successfully !!!")