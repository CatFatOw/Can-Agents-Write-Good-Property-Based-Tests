import subprocess

result = subprocess.run(
    ["mutmut", "results"],
    cwd="/Users/michaelwu/cmu-research_PBT/Can-Agents-Write-Good-Property-Based-Tests/Codex/np_testing/codex_np_mutation_testing",
    capture_output=True,
    text=True
)

mutant_id = "numpy.linalg._linalg.x__assert_stacked_square__mutmut_3"
show = subprocess.run(
    ["mutmut", "show", mutant_id],
    cwd="/Users/michaelwu/cmu-research_PBT/Can-Agents-Write-Good-Property-Based-Tests/Codex/np_testing/codex_np_mutation_testing",
    capture_output=True,
    text=True
)

output = result.stdout
print(output)
for survived in output.splitlines():
    print(survived)
    print(survived.split(":")[0])
    print("we breaked!")
    break
#print(show.stdout)
