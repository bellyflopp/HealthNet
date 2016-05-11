#Autogenerated by ReportLab guiedit do not edit
from HealthNet.static.reportlab.graphics.charts.piecharts import Pie
from HealthNet.static.reportlab.graphics.widgets.grids import ShadedRect
from HealthNet.static.reportlab.graphics.charts.legends import Legend
from HealthNet.static.reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, String
from HealthNet.static.reportlab.graphics.charts.textlabels import Label
from HealthNet.static.reportlab.graphics.samples.excelcolors import *

class SimplePie(_DrawingEditorMixin,Drawing):
    def __init__(self,width=200,height=150,*args,**kw):
        Drawing.__init__(self,width,height,*args,**kw)
        self._add(self,Pie(),name='chart',validate=None,desc="The main chart")
        self.chart.width      = 100
        self.chart.height     = 100
        self.chart.x          = 25
        self.chart.y          = 25
        self.chart.slices[0].fillColor = color01
        self.chart.slices[1].fillColor = color02
        self.chart.slices[2].fillColor = color03
        self.chart.slices[3].fillColor = color04
        self.chart.slices[4].fillColor = color05
        self.chart.slices[5].fillColor = color06
        self.chart.slices[6].fillColor = color07
        self.chart.slices[7].fillColor = color08
        self.chart.slices[8].fillColor = color09
        self.chart.slices[9].fillColor = color10
        self.chart.data                = (100, 150, 180)
        self._add(self,Label(),name='Title',validate=None,desc="The title at the top of the chart")
        self.Title.fontName   = 'Helvetica-Bold'
        self.Title.fontSize   = 7
        self.Title.x          = 100
        self.Title.y          = 135
        self.Title._text      = 'Chart Title'
        self.Title.maxWidth   = 180
        self.Title.height     = 20
        self.Title.textAnchor ='middle'
        self._add(self,Legend(),name='Legend',validate=None,desc="The legend or key for the chart")
        self.Legend.colorNamePairs = [(color01, 'North'), (color02, 'South'),(color03, 'Central')]
        self.Legend.fontName       = 'Helvetica'
        self.Legend.fontSize       = 7
        self.Legend.x              = 160
        self.Legend.y              = 85
        self.Legend.dxTextSpace    = 5
        self.Legend.dy             = 5
        self.Legend.dx             = 5
        self.Legend.deltay         = 5
        self.Legend.alignment      ='right'
        self.chart.slices.strokeWidth  = 1
        self.chart.slices.fontName     = 'Helvetica'
        self.background                = ShadedRect()
        self.background.fillColorStart = backgroundGrey
        self.background.fillColorEnd   = backgroundGrey
        self.background.numShades      = 1
        self.background.strokeWidth    = 0.5
        self.background.x              = 25
        self.background.y              = 25
        self.Legend.columnMaximum  = 10
        self._add(self,0,name='preview',validate=None,desc=None)

if __name__=="__main__": #NORUNTESTS
    SimplePie().save(formats=['pdf'],outDir=None,fnRoot=None)
