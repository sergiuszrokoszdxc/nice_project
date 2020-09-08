import React from 'react';
import './App.css';

var ScreenEnum = {
  HOME: 1,
  CREATE: 2,
  FIND: 3,
  PLAY: 4
}

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      screen: ScreenEnum.HOME,
      gameID: "g"
    }
  }

  changeScreen = (screen, gameID) => {
    this.setState({
      screen: screen,
      gameID: gameID
    })
  };

  render() {
    let component
    if (this.state.screen === ScreenEnum.HOME) {
      component = <HomeScreen changeScreen={this.changeScreen}/>
    } else if (this.state.screen === ScreenEnum.CREATE) {
      component = <CreateScreen changeScreen={this.changeScreen}/>
    } else if (this.state.screen === ScreenEnum.FIND) {
      component = <FindScreen changeScreen={this.changeScreen}/>
    } else if (this.state.screen === ScreenEnum.PLAY) {
      component = <PlayScreen gameID={this.state.gameID} changeScreen={this.changeScreen}/>
    }
    return (
      <div>
        <div>MASTERMIND</div>
        {component}
      </div>
    )
  }
}

class HomeScreen extends React.Component {
  render() {
    return (
      <div>
        <div onClick={() => this.props.changeScreen(ScreenEnum.CREATE, "")}>
          # Create new game.
        </div>
        <div onClick={() => this.props.changeScreen(ScreenEnum.FIND, "")}>
          # Find a game.
        </div>
      </div>
    )
  }
}

class CreateScreen extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      n_colours: 1,
      n_positions: 1,
      max_tries: 1
    }
  }
  
  counterDown = (state) => {
    let new_state
    if (this.state[state] > 1) {
      new_state = this.state[state] - 1
    } else {
      new_state = 1
    }
    this.setState({
      [state]: new_state
    })
  }
  
  counterUp = (state) => {
    this.setState({
      [state]: this.state[state] + 1
    })
  }

  createGame = () => {
    const options = {
      method: "POST",
      body: JSON.stringify(this.state),
      headers: {
          'Content-Type': 'application/json'
      }
    }
    fetch("http://localhost/game", options)
      .then(res => res.json())
      .then(
        res => {
          const gameID = res.id_
          this.props.changeScreen(ScreenEnum.PLAY, gameID)
        }
      );
  }

  render() {
    const state = this.state
    const cntDwn = this.counterDown
    const cntUp = this.counterUp

    const clr_name = "Number of colours"
    const clr_cnt = state.n_colours

    const pos_name = "Number of positions"
    const pos_cnt = state.n_positions

    const max_name = "Maximal number of tries"
    const max_cnt = state.max_tries

    return (
      <div>
        <CreateOption name={clr_name} cnt={clr_cnt} 
        cntDwn={() => cntDwn("n_colours")} cntUp={() => cntUp("n_colours")}/>
        <CreateOption name={pos_name} cnt={pos_cnt} 
        cntDwn={() => cntDwn("n_positions")} cntUp={() => cntUp("n_positions")}/>
        <CreateOption name={max_name} cnt={max_cnt} 
        cntDwn={() => cntDwn("max_tries")} cntUp={() => cntUp("max_tries")}/>
        <div onClick={this.createGame}>
          # Create the game!
        </div>
        <div onClick={() => this.props.changeScreen(ScreenEnum.FIND, "")}>
          # Find an existing game.
        </div>
      </div>
    )
  }
}


class CreateOption extends React.Component {
  render() {
    const name = this.props.name
    const count = this.props.cnt
    const counterDown = this.props.cntDwn
    const counterUp = this.props.cntUp
    return (
      <div>
        <div>
          {name}: {count}
        </div>
        <button onClick={counterDown}>
          -
        </button>
        <button onClick={counterUp}>
          +
        </button>
      </div>
    )
  }
}

class FindScreen extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      games: [],
      selectedID: ""
    }
  }

  downloadGames = () => {
    fetch("http://localhost/game")
      .then(res => res.json())
      .then(
        res => {
          this.setState({
            games: res
          })
        }
      )
  }

  selectGame = (id) => {
    this.setState({
      selectedID: id
    })
  }

  chooseGame = () => {
    this.props.changeScreen(ScreenEnum.PLAY, this.state.selectedID)
  }

  componentDidMount() {
    this.downloadGames()
  }

  render() {
    let chooseButton
    if (this.state.selectedID) {
      chooseButton = (
        <div onClick={this.chooseGame}>
          # Choose the game!
        </div>
      )
    }
    return (
      <div>
        {
          this.state.games.map((data) => {
            let selected
            if (data.id_ === this.state.selectedID) {
              selected = true
            } else {
              selected = false
            }
            return <FindRow select={this.selectGame} data={data} selected={selected}/>
          })
        }
        <div onClick={this.downloadGames}>
          # Refresh
        </div>
        <div onClick={() => this.props.changeScreen(ScreenEnum.CREATE, "")}>
          # Create new game.
        </div>
        {chooseButton}
      </div>
    )
  }
}

class FindRow extends React.Component {
  render() {
    const gameID = this.props.data.id_
    const n_colours = this.props.data.n_colours
    const n_positions = this.props.data.n_positions
    const max_tries = this.props.data.max_tries
    let selected
    if (this.props.selected) {
      selected = "TICK!"
    } else {
      selected = ""
    }
    return (
      <div onClick={() => this.props.select(gameID)}>
        <div>
          Number of colours: {n_colours}
        </div>
        <div>
          Number of positions: {n_positions}
        </div>
        <div>
          Maximal number of tries: {max_tries}
        </div>
        <div>
          Selected: {selected}
        </div>
        <div>
          ====================================
        </div>
      </div>
    )
  }
}


class PlayScreen extends React.Component {
  constructor(props) {
    super(props)
    const history = []
    this.state = {
      guess: [],
      history: history,
      has_ended: false,
      win: false,
      n_colours: 1,
      n_positions: 1,
      max_tries: 1,
      msg: "Welcome to the game!"
    }
  }

  getInitialGuess = (history, n_positions) => {
    if (history.length > 0) {
      return history[history.length - 1].guess
    } else {
      return Array.from(Array(n_positions), () => 0)
    }
  }

  downloadData = () => {
    fetch(`http://localhost/game/${this.props.gameID}`)
      .then(res => res.json())
      .then(
        res => {
          const guess = this.getInitialGuess(res.history, res.n_positions)
          let msg
          if (res.win_token) {
            msg = "Congratulations. You won!"
          } else if (res.has_ended) {
            msg = "The game has ended."
          } else {
            msg = "Try to guess the secret sequence."
          }
          this.setState({
            guess: guess,
            history: res.history,
            has_ended: res.has_ended,
            win: res.win_token,
            n_colours: res.n_colours,
            n_positions: res.n_positions,
            max_tries: res.max_tries,
            msg: msg
          });
        }
      )
  }

  sendGuess = () => {
    const options = {
      method: "POST",
      body: JSON.stringify({guess: this.state.guess}),
      headers: {
          'Content-Type': 'application/json'
      }
    }
    fetch(`http://localhost/game/${this.props.gameID}`, options)
      .then(res => res.json())
      .then(
        res => {
          const guess = this.getInitialGuess(res.history, res.n_positions)
          let msg
          if (res.win_token) {
            msg = "Congratulations. You won!"
          } else if (res.has_ended) {
            msg = "The game has ended."
          } else {
            msg = "Try to guess the secret sequence."
          }
          this.setState({
            guess: guess,
            history: res.history,
            has_ended: res.has_ended,
            win: res.win_token,
            n_colours: res.n_colours,
            n_positions: res.n_positions,
            max_tries: res.max_tries,
            msg: msg
          });
        }
      )
  }

  changePinValue = (i) => {
    const value = this.state.guess[i]
    const newValue = (value + 1) % this.state.n_colours
    const newArray = this.state.guess.slice()
    newArray[i] = newValue
    this.setState({
      guess: newArray
    })
  }

  componentDidMount() {
    this.downloadData()
  }

  render() {
    return (
      <div>
        <div>
          {this.state.msg}
        </div>
        <div>
          {
            this.state.history.map((history) => {
              return <HistoryRow history={history}/>
            })
          }
        </div>
        <GuessPanel
          guess={this.state.guess}
          onButtonClick={() => this.sendGuess()}
          onPinClick={(i) => this.changePinValue(i)}
        />
        <div onClick={() => this.props.changeScreen(ScreenEnum.CREATE, "")}>
          # Create new game.
        </div>
        <div onClick={() => this.props.changeScreen(ScreenEnum.FIND, "")}>
          # Find a game.
        </div>
      </div>
    )
  }
}

class HistoryRow extends React.Component {
  render () {
    const sequence = this.props.history.guess
    const hint = this.props.history.hint
    return (
      <div>
        <HistorySequence sequence={sequence}/>
        <HistoryHint hint={hint}/>
        <div>
          ====================================
        </div>
      </div>
    )
  }
}

class HistorySequence extends React.Component {
  render () {
    return (
      <div>
        {this.props.sequence}
      </div>
    )
  }
}

class HistoryHint extends React.Component {
  render () {
    return (
      <div>
        Good Position: {this.props.hint[0]}, Good Colour: {this.props.hint[1]}
      </div>
    )
  }
}

class GuessPanel extends React.Component {
  render() {
    const guess = this.props.guess
    const guessPins = []
    for (let i = 0; i < guess.length; i++) {
      guessPins.push(<GuessPin value={guess[i]} onClick={() => this.props.onPinClick(i)}/>)
    }
    return (
      <div>
        {guessPins}
        <button onClick={() => this.props.onButtonClick()}>
          Submit!
        </button>
      </div>
    )
  }
}

class GuessPin extends React.Component {
  render() {
    const value = this.props.value
    return (
      <button onClick={() => this.props.onClick()}>
        {value}
      </button>
    )
  }
}

export default App;
