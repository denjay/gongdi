import axios from 'axios'
import danti from './danti'

const state = ()=>{
    return {buweis:[]}
}

const getters = {
    buweis:state=>{
        return state.buweis
    }
}

const  mutations = {
    setBuweis(state, data){
        state.buweis = data
    },
    removeBuweis(state,data){
        var index = state.buweis.indexOf(data)
        state.buweis.splice(index,1)
    },
}

const actions = {
    getBuweis({commit},data){
        axios.get(`/kong/gongdi_mng/v1.0/dantis/${data}/buweis`)
        .then(response=>{
            if(response.status === 200){
                commit('setBuweis',response.data)
            }
        })
    },
    postBuweis({commit,getters},data){
        axios.post('/kong/gongdi_mng/v1.0/buweis',data)
		.then(response => {
            if (response.status === 201) {
                var buweis = getters.buweis 
                buweis.unshift(response.data)
                commit('setBuweis', buweis)
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putBuweis({commit,getters},data){
        delete data.danti_name
        delete data.dantiid
        axios.put(`/kong/gongdi_mng/v1.0/buweis/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                for(var item of getters.buweis){
                    if(item.id === data.id){
                        var index = getters.buweis.indexOf(item)
                        var [...newDatas] = getters.buweis
                        newDatas.splice(index, 1, response.data)
                        commit('setBuweis',newDatas)
                        break
                    }
                }
            }
        })
        .catch(error => {
            alert('出错')
        })
    },
    removeBuweis({commit},data){
        axios.delete(`/kong/gongdi_mng/v1.0/buweis/${data.id}`)
			.then(function(response){
                if(response.status === 204){
                    commit('removeBuweis',data)
                }
			}).catch(function(error){
			})
    }
}

export default {
    namespaced: true,    
    state,
    getters,
    mutations,
    actions,
    modules:{danti}
}