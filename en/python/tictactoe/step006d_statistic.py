"""AI test for playing different TicTacToe-AI's versus each other.
   prints the output into the file output.csv
   This code must be in the same place as step006c_paramters.py
   If pygal is correctly installed, also creates .svg graphics
   If you want graphics, install pygal, see http://www.pygal.org"""
import step006c_parameters
graphic = True
try:
    import pygal
except ModuleNotFoundError:
    graphic = False

pairings = [("easy", "easy"),
            ("easy", "medium"),
            ("easy", "hard"),
            ("medium", "easy"),
            ("medium", "medium"),
            ("medium", "hard"),
            ("hard", "easy"),
            ("hard", "medium"),
            ("hard", "hard"),
           ]
with open("output.csv", "w") as csvfile: # open in write mode (overwriting)
    csvfile.write("pairing, wins, losses, draws,\n")  # write csv header line
for pair in pairings:
    winners = {1:0, 2:0, 3:0}
    runs = 5000      # number of games each AI pair must play
    for i in range(runs):
        result = step006c_parameters.game(pair[0], pair[1], True)
        winners[result] += 1
    #print(winners)
    print(f"{pair[0]} vs {pair[1]}: wins:{winners[1]} losses:{winners[2]} draws:{[winners[3]]}")
    if graphic:
        # ---- create pygal chart and save it as .svg file -----
        # ----(linux users: open the .svg it with browser!) -----
        pie_chart = pygal.Pie(half_pie=True, legend_at_bottom=True)
        pie_chart.title = "TicTacToe ({} runs): {} vs. {}".format(
            str(runs/1000)+"k" if runs > 1000 else runs, pair[0], pair[1])
        pie_chart.add('wins: {} ({:.1f}%)'.format(winners[1], winners[1]/runs*100), winners[1])
        pie_chart.add('losses: {} ({:.1f}%)'.format(winners[2], winners[2]/runs*100), winners[2])
        pie_chart.add('draws: {} ({:.1f}%)'.format(winners[3], winners[3]/runs*100), winners[3])
        pie_chart.render_to_file(f'tictactoe{runs}_{pair[0]}_vs_{pair[1]}.svg')
        # --------- add line to output file -----
    with open("output.csv", "a") as csvfile:  # open in append mode
        csvfile.write("{} vs {}:,{},{},{},\n".format(
            pair[0],  pair[1], winners[1], winners[2], winners[3]))

print("finished! see output.csv")
