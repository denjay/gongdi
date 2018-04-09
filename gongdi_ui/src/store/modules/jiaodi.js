import axios from 'axios'
import buwei from './buwei'

const state = ()=>{
    return {jiaodis:[],total_datas:null}
}

const getters = {
    jiaodis:state=>{
        return state.jiaodis
    },
    total_datas:state=>{
        return state.total_datas
    }
}

const  mutations = {
    setJiaodis(state, data){
        state.jiaodis = data
    },
    removeJiaodis(state,data){
        var index = state.jiaodis.indexOf(data)
        state.jiaodis.splice(index,1)
    },
    setTotalDatas(state, data){
        state.total_datas = data
    },
}

const actions = {
    getJiaodis({commit},data){
        var query_args = ''
        for(var key in data){
            if(Boolean(data[key])){
                query_args += `&${key}=${data[key]}`
            }
        }
        axios.get(`/kong/gongdi_mng/v1.0/jiaodi_docs?${query_args}`)
        .then(response=>{
            if(response.status === 200){
                commit('setJiaodis',response.data)
                // 获取数据条数
                var total = response.headers["x-total"]       
                commit("setTotalDatas",total)
            }
        }).catch(function(error){
			alert('getJiaodis失败')
		})
    },
    postJiaodis({commit,getters},data){
        axios.post('/kong/gongdi_mng/v1.0/jiaodi_docs',data)
		.then(response => {
            if (response.status === 201) {
                var [...jiaodi] = getters.jiaodis 
                jiaodi.unshift(response.data)
                commit('setJiaodis', jiaodi)
            }
		}).catch(function(error){
			alert('postJiaodis失败')
		})
    },
    putJiaodis({commit,getters},data){
        axios.put(`/kong/gongdi_mng/v1.0/jiaodi_docs/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                for(var item of getters.jiaodis){
                    if(item.id === data.id){
                        var index = getters.jiaodis.indexOf(item)
                        var [...jiaodis] = getters.jiaodis
                        jiaodis.splice(index, 1, response.data)
                        commit('setJiaodis',jiaodis)
                        break
                    }
                }
            }
        }).catch(error => {
            alert('putJiaodis出错')
        })
    },
    removeJiaodis({commit},data){
        axios.delete(`/kong/gongdi_mng/v1.0/jiaodi_docs/${data.id}`)
        // .then(function(response){
        //     if(response.status === 204){
        //         commit('removeJiaodis',data)
        //     }
        // })
        .catch(function(error){
            alert('removeJiaodis出错')
        })
    }
}

export default {
    namespaced: true,    
    state,
    getters,
    mutations,
    actions,
    modules:{buwei}
}