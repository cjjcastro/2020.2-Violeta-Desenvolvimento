import React, { Component } from 'react';
import './App.css';
import Header from './components/header';
import Home from './components/home';
import Questionario from './components/questionario';
import Footer from './components/footer';

class App extends Component {
    render() {
        return (
            <div>
                <Header />
                <Home />
                <Questionario />
                <Footer />
            </div>
        );
    }
}
export default App;
