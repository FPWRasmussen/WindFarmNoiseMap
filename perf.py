from line_profiler import LineProfiler
from main import main

lprofiler = LineProfiler()

lp_wrapper = lprofiler(main)

lp_wrapper()

lprofiler.print_stats()