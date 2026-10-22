"""全书分枝交汇图入口。"""
import sys
sys.dont_write_bytecode = True
from rebuild_plot_topology import prepare, render

if __name__ == "__main__":
    prepare() if "--prepare" in sys.argv else render()
