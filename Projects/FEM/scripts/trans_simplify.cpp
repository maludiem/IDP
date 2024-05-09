#include <vtkSmartPointer.h>
#include <vtkOBJReader.h>
#include <vtkPolyData.h>
#include <vtkDecimatePro.h>
#include <vtkPolyDataWriter.h>

int main(int argc, char* argv[])
{
    // ��ȡOBJ�ļ�
    vtkSmartPointer<vtkOBJReader> reader = vtkSmartPointer<vtkOBJReader>::New();
    reader->SetFileName("./output/main_model/model_p.obj");
    reader->Update();

    // ������ģ�͵Ķ���
    vtkSmartPointer<vtkDecimatePro> decimate = vtkSmartPointer<vtkDecimatePro>::New();
    decimate->SetInputConnection(reader->GetOutputPort());
    decimate->SetTargetReduction(0.5); // ���ü򻯵ĳ̶ȣ�0.5��ʾ����50%��������
    decimate->Update();

    // д��VTK�ļ�
    vtkSmartPointer<vtkPolyDataWriter> writer = vtkSmartPointer<vtkPolyDataWriter>::New();
    writer->SetFileName("./output/main_model/model_p.vtk");
    writer->SetInputConnection(decimate->GetOutputPort());
    writer->Write();

    return 0;
}
