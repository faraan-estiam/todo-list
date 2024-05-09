'use client'
import { useState } from "react";
import axios from "axios";
import { url } from "inspector";
import { headers } from "next/headers";

const api = axios.create({
  baseURL: "http://localhost:8000"
})

export default function Home() {
  const [ token, setToken ] = useState('NONE')
  const [ data, setData ] = useState([])

  if (token == 'NONE') {
    return (
      <div className="loginform">
        <label htmlFor="usrname">Email</label>
        <input type="email" name="usrname" id="usrname" />
        <label htmlFor="pswrd">Password</label>
        <input type="password" name="pswrd" id="pswrd" />
        <button type="button" onClick={()=>login(setToken)}>login</button>
      </div>
    )
  } else if(data.length == 0) {
    build_todos(token, setData)
  } else {
    return <>{data}</>
  }
}


function login(setToken:Function) {
  const username = (document.getElementById("usrname") as HTMLInputElement).value
  const password = (document.getElementById("pswrd") as HTMLInputElement).value
  api.post(
    "/auth/login",
    {
      "username": username,
      "password": password
    },
    {
      "headers":
      {
        "content-type": "application/x-www-form-urlencoded"
      }
    }
  ).then((response) => {
    setToken(`Bearer ${response.data.access_token}`)
  }).catch((error) => {
    console.error(error)
  })
}

function build_todos(token:string, setData:Function) {
    api.get(
      "/todos",
      {
        "headers":
        {
          "Authorization" : token
        }
      }
    ).then((response) => {
      let data = response.data as Array<Task>
      let result = []
      for (let i=0; i<data.length; i++) {
        let title = data[i].title
        let description = data[i].description
        let status = data[i].status
        result.push(<p id={"task_" + i} className={"status_"+status}>{title}</p>)
      }
      setData(result)
    }).catch((error) => {
      console.error(error)
    })
}

type Task = {
  title:string,
  description:string,
  status:number
}
