from pyscript.web import page, div, input_, button, img, span, wrap_dom_element
from pyscript import display



class NavTabs:
    VISIBLE = "display: block;"
    SELECTED = "font-weight: bold; background-color: lightgray;"
    DEFAULT = ""

    def __init__(self):
        self.state = 0
        self.nav_list = page["nav ul"][0]
        self.content = page["#tab_content"][0]
        self.hide_btn = page["#tab_hide"][0]
        
        self.hide_btn.onclick = lambda e: self.hideContent()
        for ch in self.nav_list.children:
            ch.onclick = self.onTabClick

    def getContentDiv(self, num):
        return self.content.children[num - 1]
    
    def getNavTitle(self, num):
        return self.nav_list.children[num - 1]
    
    def showContent(self, num):
        self.getNavTitle(num).style = NavTabs.SELECTED 
        self.getContentDiv(num).style = NavTabs.VISIBLE
        self.hide_btn.style = NavTabs.VISIBLE
        self.state = num

    def hideContent(self):
        if self.state:
            self.getNavTitle(self.state).style = NavTabs.DEFAULT
            self.getContentDiv(self.state).style = NavTabs.DEFAULT
            self.hide_btn.style = NavTabs.DEFAULT
            self.state = 0
    
    def onTabClick(self, e):
        clicked_tab = int(wrap_dom_element(e.target).id[-1])
        if self.state == clicked_tab:
            self.hideContent()
            return
        self.hideContent()
        self.showContent(clicked_tab)
