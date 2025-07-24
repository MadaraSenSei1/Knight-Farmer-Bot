import React,{useState, useEffect} from 'react';
import RegisterPage from './component/RegisterPage/RegisterPage';
import Header from './component/Header/Header';
import Accounts from './component/AccountsPage/Accounts';
import { io } from "socket.io-client";
import { Context } from './context';
import {Route, Routes} from 'react-router-dom'
// import logo from './logo.svg';
import './App.css';
import TravianBot from './component/BotPage/TravianBot';
import Raids from './component/BotPage/raids/Raids';
import Troops from './component/BotPage/troops/Troops';
import SearchFarmList from './component/BotPage/searchFarm/SearchFarmList';
const socket = io("https://farmer.bot.biz.ua");
function App() {
  const [arrowBackStatus, setArrowBackStatus] = useState('/')
  const [answer_travianbot_socket, set_answer_travianbot_socket] = useState('Accounts (Ver:3.0.5)')
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 1000);
  const [arr_logs, set_arr_logs] = useState([])
  const [socket_model, set_socket_model] = useState(false)
  const [security_bot, set_security_bot] = useState(false)
  const [props_token, set_props_token] = useState('')
 
  useEffect(() => {
    socket.on("connect", () => {  
      console.log('connect to server')
    }); 
    socket.on("disconnect", () => {
        console.log(socket.id); // undefined
    });
  
    socket.on('travian bot answer', (data) => {
        set_arr_logs((prev => {
          return [data, ...prev];
        }))
    })
    let get_token = localStorage.getItem("token_Account_bot")
    set_props_token(get_token)
  },[])




  return (
    
    <Context.Provider value={{
      socket
    }}> 
      {isMobile && <div className="App container">
      <Header setArrowBackStatus={setArrowBackStatus} socket={socket} set_socket_model={set_socket_model} answer_travianbot_socket={answer_travianbot_socket} arrowBackStatus={arrowBackStatus}/>
      {socket_model ?
                   <div style={{height:"100vh",backgroundColor:"rgba(0,0,0,0.7)",marginLeft:10, marginRight:10 }}>
                   <div style={{overflowY:"scroll"}}>
                     {arr_logs.map((item, idx) => {
                       return (
                         <div style={{color:"white", paddingLeft:14, fontSize:14}} key={idx}>
                           {item}
                         </div>
                       )
                     })}
                   </div>
                 </div>
       :
       <Routes>
          <Route path='/' element={<Accounts security_bot={security_bot} set_security_bot={set_security_bot} setArrowBackStatus={setArrowBackStatus}/>}/>
          <Route path='/registerUser' element={<RegisterPage/>}/>
          <Route path='/travianbot' element={<TravianBot setArrowBackStatus={setArrowBackStatus}/>}/>
          <Route path='/troops' element={<Troops/>}/>
          <Route path='/raids' element={<Raids token={props_token}/>}/>
          <Route path='/searchFarmList' element={<SearchFarmList server="ts1.x1.europe.travian.com" coordinates="(46|-71)" token={props_token}/>}/>
      </Routes>
       }

        
        {/* {!registerPageModuleStatus && }
        {registerPageModuleStatus && }  */}
        {/* <TravianBot/> */}
      </div>}
    </Context.Provider>
  );
}

export default App;
