import axios from 'axios'

const state = {
    buweis:[],
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
                data = getters.buweis 
                data.unshift(response.data)
                commit('setBuweis', data)
            }
            else {
                alert('新增失败')
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putBuweis({commit,getters},data){
        console.table(data)
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
    state,
    getters,
    mutations,
    actions
}