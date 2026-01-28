import wx
import wxOpenGL

material = wxOpenGL.PlasticMaterial([0.4, 0.4, 0.4, 1.0])
selected_material = wxOpenGL.PlasticMaterial([1.0, 0.5, 0.5, 1.0])
point = wxOpenGL.Point(0, 30, 50)
angle = wxOpenGL.Angle.from_euler(45.0, 270.0, 0.0)

selected_material.x_ray = True


class Frame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, size=(1600, 900))
        self.canvas = wxOpenGL.Canvas(self)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.canvas, 1, wx.EXPAND)
        vsizer.Add(hsizer, 1, wx.EXPAND)
        self.SetSizer(vsizer)

        self.model = wxOpenGL.MeshModel(self.canvas, material, selected_material, False,
                           r'C:\Users\drsch\PycharmProjects\harness_designer\scratches\15326864_3D_STP.stp',
                           point, angle)


class App(wx.App):

    def OnInit(self):
        self.frame = Frame()
        self.frame.Show()

        return True


app = App()
app.MainLoop()

