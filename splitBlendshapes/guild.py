import sys
sbb_path = r'D:\codes\dev\splitBlendshapes'
if not sbb_path in sys.path:
    sys.path.append(sbb_path)
    
import sbb_UI
sbb_UI.main()