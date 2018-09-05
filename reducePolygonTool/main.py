import sys
rpt_path = r'D:\codes\dev\reducePolygonTool'
if not rpt_path in sys.path:
    sys.path.append(rpt_path)

import UI
UI.main()