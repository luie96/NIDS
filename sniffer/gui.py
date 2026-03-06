import wx
import wx.grid as gridlib


def __init__(self):
    super().__init__(None, title="日志表格", size=(800, 600))
    
    # 创建面板
    panel = wx.Panel(self)
    
    # 创建表格
    self.table = gridlib.Grid(panel)
    self.table.CreateGrid(0, 6)  # 初始行数为0，列数为6
    
    # 设置表格列标题
    columns = ["时间", "源 IP", "目标 IP", "协议", "动作", "信息"]
    for i, col_name in enumerate(columns):
        self.table.SetColLabelValue(i, col_name)
    
    # 设置表格布局
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.table, 1, wx.ALL | wx.EXPAND, 5)
    panel.SetSizer(sizer)
    
    # 绑定窗口关闭事件
    self.Bind(wx.EVT_CLOSE, self.OnClose)

def update_gui(self, matches):
    # 如果有现有行，先删除它们
    if self.table.GetNumberRows() > 0:
        self.table.DeleteRows(0, self.table.GetNumberRows())
    
    # 插入新行
    if matches:
        self.table.AppendRows(len(matches))
    
    # 更新数据
    for row, match in enumerate(matches):
        self.table.SetCellValue(row, 0, match["Time"])
        self.table.SetCellValue(row, 1, match["Source IP"])
        self.table.SetCellValue(row, 2, match["Destination IP"])
        self.table.SetCellValue(row, 3, match["Protocol"])
        self.table.SetCellValue(row, 4, match["Action"])
        self.table.SetCellValue(row, 5, match["Message"])
    
    # 调整列宽
    for col in range(self.table.GetNumberCols()):
        self.table.AutoSizeColumn(col)

def OnClose(self, event):
    self.Destroy()

# # 示例数据
# matches = [
#     {
#         "Time": "2023-10-10 12:00:00",
#         "Source IP": "192.168.1.1",
#         "Destination IP": "192.168.1.2",
#         "Protocol": "TCP",
#         "Action": "允许",
#         "Message": "正常连接"
#     },
#     {
#         "Time": "2023-10-10 12:01:00",
#         "Source IP": "192.168.1.3",
#         "Destination IP": "192.168.1.4",
#         "Protocol": "UDP",
#         "Action": "拒绝",
#         "Message": "异常连接"
#     }
# ]

# # 创建应用和窗口
# app = wx.App()
# frame = MyFrame()
# frame.Show()

# # 更新表格内容
# frame.update_gui(matches)

# # 运行应用主循环
# app.MainLoop()