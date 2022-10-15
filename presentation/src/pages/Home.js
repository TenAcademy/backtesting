import React, { useEffect, useState } from 'react'
import "./bootstrap.css"
import axiosInstance from '../api';
import axios from 'axios';
const _ = require('lodash');


const Home = () => {

    const [result, setresult] = useState({})
    // const [assets, setassets] = useState([])

    const assets =[
        {"name":"Bitcoin","symb":"BTC"},
        {"name":"Netflix","symb":"NFLX"},
        {"name":"Microsoft","symb":"MFST"}
    ]

    
    // useEffect( () => {
    //     // const getAssets = async () => {
    //         let params = {
    //             headers: {
    //                 "X-CoinAPI-Key": "379C1675-45EB-42DF-9CCA-DBBC66125710"
    //             }
    //         }
    //         let response = axios.get("https://rest.coinapi.io/v1/assets", params).then((response)=>setassets([...response.data])).then(console.log("done")).catch(console.error)
    //         // let data = response.data
    
    //         // setassets({ ...data })
    //     // };
    // //    getAssets().then((data)=>console.log(data)).catch(console.error)
    // }, [])


    const show_assets = () => {

        // let sortedAssets=_.sortBy([...assets],"name");
        // console.log(assets[0]);
        const options = [...assets].map((e) => {
            return <option key={e.symb} defaultValue={e.symb}>{e.name}</option>
        })
        return options

    }

    const test = async (e) => {
        e.preventDefault()
        let asset = document.querySelector("#asset").value
        let strategy = document.querySelector("#strategy").value
        let start = document.querySelector("#start").value
        let end = document.querySelector("#end").value
        let cash = document.querySelector("#cash").value

        let params = {
            start_date: start,
            end_date: end,
            asset: asset,
            cash: parseInt(cash),
            strategy: strategy
        }
        console.log(params);

        let response = await axiosInstance.post("/backtest", params)
        // console.log(response.data);
        setresult({ ...response.data })

    }
    const logout = (e) => {
        e.preventDefault()
        window.localStorage.clear()
        window.location = "/"
    }

    return (
        <div>

            <button className='btn btn-secondary' onClick={logout} style={{ "position": "absolute", "top": "10px", "right": "10px" }}>Log out</button>

            <div className="d-flex w-100">
                <form action="" onSubmit={test}>
                    <div className='my-2'>

                        <select className='form-control' name="asset" id="asset">
                            {/* {show_assets()} */}
                            <option value="BTC">Bitcoin</option>
                            <option value="NFLX">Netflix</option>
                            <option value="MSFT">Microsoft</option>
                        </select>
                        {/* <input className='form-control' type="text" name="" id="asset" placeholder='asset' /> */}
                    </div>
                    <div className='my-2'>

                        <select className='form-control' name="" id="strategy" required>
                            <option value=""></option>
                            <option value="test">Test Strategy</option>
                            <option value="sma">SMA</option>
                            <option value="sma_rsi">SMA with RSI</option>
                        </select>
                    </div>

                    <div className='my-2'>

                        <input className='form-control' type="date" name="" id="start" placeholder='YYYY-mm-dd' />
                    </div>

                    <div className='my-2'>

                        <input className='form-control' type="date" name="" id="end" placeholder='YYYY-mm-dd' />
                    </div>

                    <div className='my-2'>

                        <input className='form-control' type="text" name="" id="cash" placeholder='cash' />
                    </div>
                    <div className='my-2'>
                        <input type="submit" className='btn btn-primary px-3' value={"Run Test"} />
                    </div>
                </form>
                <div className="px-2 ml-1" style={{ "border": "1px solid black", "borderRadius": "5px", "width": "400px" }}>

                    <table className='table table-bg table-stripe'>
                        <thead>
                            <tr>
                                <th>
                                    Metric
                                </th>
                                <th>
                                    Value
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th>Sharpe Ratio</th>
                                <td>{result.sharpe_ratio}</td>
                            </tr>
                            <tr>
                                <th>Return</th>
                                <td>{result.return}</td>
                            </tr>
                            <tr>
                                <th>Max drawdown</th>
                                <td>{result.max_drawdown}</td>
                            </tr>
                            <tr>
                                <th>Win Trade</th>
                                <td>{result.win_trade}</td>
                            </tr>
                            <tr>
                                <th>Loss Trade</th>
                                <td>{result.loss_trade}</td>
                            </tr>
                            <tr>
                                <th>Total Trade</th>
                                <td>{result.total_trade}</td>
                            </tr>
                            <tr>
                                <th>Start Portfolio</th>
                                <td>{result.start_portfolio}</td>
                            </tr>
                            <tr>
                                <th>Final Portfolio</th>
                                <td>{result.final_portfolio}</td>
                            </tr>
                        </tbody>
                    </table>

                </div>
            </div>


        </div>
    )
}

export default Home