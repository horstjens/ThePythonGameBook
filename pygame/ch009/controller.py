class Controller(object):
  """Global game control"""

  def __init__(self, view, maps, config):

    self.view = view(self, config)
    self.game = MazeGame(maps, config)
    self.game.reset(START)
    self.state = 'playing'


  def dispatch(self, all_events):
    """Control the game state."""

    event, move_events = all_events
    if event == 'quit':
      self.game.quit()
      return False

    if self.state == 'playing':
      self.state = self.game.process(self.view, move_events)
      return True

    if self.state == 'ending':
      self.game.wait(self.view)
      if event == 'other_key':
        self.state = 'playing'
        self.game.reset(START)

    return True


  def run(self):

    self.view.run()

