import wx
import wxOpenGL


class Frame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, size=(800, 600))
        self.canvas = wxOpenGL.Canvas(self)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.canvas, 1, wx.EXPAND)
        vsizer.Add(hsizer, 1, wx.EXPAND)
        self.SetSizer(vsizer)


class App(wx.App):

    def OnInit(self):
        self.frame = Frame()
        self.frame.Show()

        return True


app = App()
app.MainLoop()

