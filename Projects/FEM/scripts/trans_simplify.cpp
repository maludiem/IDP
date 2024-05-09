#include <vtkSmartPointer.h>
#include <vtkOBJReader.h>
#include <vtkPolyData.h>
#include <vtkDecimatePro.h>
#include <vtkPolyDataWriter.h>

int main(int argc, char* argv[])
{
    // 读取OBJ文件
    vtkSmartPointer<vtkOBJReader> reader = vtkSmartPointer<vtkOBJReader>::New();
    reader->SetFileName("./output/main_model/model_p.obj");
    reader->Update();

    // 创建简化模型的对象
    vtkSmartPointer<vtkDecimatePro> decimate = vtkSmartPointer<vtkDecimatePro>::New();
    decimate->SetInputConnection(reader->GetOutputPort());
    decimate->SetTargetReduction(0.5); // 设置简化的程度，0.5表示减少50%的三角形
    decimate->Update();

    // 写入VTK文件
    vtkSmartPointer<vtkPolyDataWriter> writer = vtkSmartPointer<vtkPolyDataWriter>::New();
    writer->SetFileName("./output/main_model/model_p.vtk");
    writer->SetInputConnection(decimate->GetOutputPort());
    writer->Write();

    return 0;
}
