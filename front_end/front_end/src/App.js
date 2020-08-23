import React from 'react';
import logo from './logo.svg';
import './App.css';

const colours = [
  "Tomato",
  "Orange",
  "Blue",
  "Yellow",
  "MediumSeaGreen"
];

function App() {
  return (
    <GameBox/>
  );
}

class GameBox extends React.Component {
  constructor(props) {
    super(props)
    const history = []
    const guess = this.getGuess(history)
    this.state = {
      history: history,
      msg: "Welcome to the game! Try guessing the sequence.",
      guess: guess
    }
  }

  getGuess(history) {
    if (history.length > 0) {
      return history[history.length - 1][0]
    } else {
      return [0, 0, 0, 0]
    };
  }

  getHistory() {
    fetch("http://127.0.0.1:8000/test")
      .then(res => res.json())
      .then(
        result => {
          const guess = this.getGuess(result.history)
          this.setState({
            history: result.history,
            msg: result.msg,
            guess: guess,
          });
        }
      )
  }

  sendGuess() {
    const options = {
      method: "POST",
      body: JSON.stringify(this.state.guess),
      headers: {
          'Content-Type': 'application/json'
      }
    }
    fetch("http://127.0.0.1:8000/test", options)
      .then(res => res.json());
    this.getHistory()
  }

  changePinValue(i) {
    const value = this.state.guess[i]
    const newValue = (value + 1) % 5
    const newArray = this.state.guess.slice()
    newArray[i] = newValue
    this.setState({
      guess: newArray
    })
  }

  componentDidMount() {
    this.getHistory()
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
      </div>
    )
  }
}

class HistoryRow extends React.Component {
  render () {
    const sequence = this.props.history[0]
    const hint = this.props.history[1]
    return (
      <div>
        <HistorySequence sequence={sequence}/>
        <HistoryHint hint={hint}/>
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
    return (
      <div>
        <GuessPin value={guess[0]} onClick={() => this.props.onPinClick(0)}/>
        <GuessPin value={guess[1]} onClick={() => this.props.onPinClick(1)}/>
        <GuessPin value={guess[2]} onClick={() => this.props.onPinClick(2)}/>
        <GuessPin value={guess[3]} onClick={() => this.props.onPinClick(3)}/>
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
