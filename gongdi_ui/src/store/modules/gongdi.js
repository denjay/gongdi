import axios from 'axios'

const state = {
    gongdis: [],
}

const getters = {
    gongdis:state=>{
		return state.gongdis;
    }
}

const  mutations = {
    setGongdis(state, data){
        state.gongdis = data
    },
    removeGongdi(state,data){
        var index = state.gongdis.indexOf(data)
        state.gongdis.splice(index,1)
    },
}

const actions = {
    getGongdis({commit},data){
        axios.get(`/kong/gongdi_mng/v1.0/companys/${data}/gongdis`)
		.then(response => {
            if(response.data.length === 0){
                commit('setGongdis',[])
            }
            else {
                commit('setGongdis',[response.data])
            }
		}).catch(function(error){
			console.log("actions");
		})
    },
    postGongdis({commit,getters},data){
        axios.post('/kong/gongdi_mng/v1.0/gongdis',data)
		.then(response => {
            if (response.status === 201) {
                data = getters.gongdis
                data.unshift(response.data)
                commit('setGongdis', data)
            }
            else {
                alert('新增失败')
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putGongdis({commit,getters},data){
        delete data.comp_name
        delete data.gongdiid
        if (data.starttime === null){
            data.starttime = ""
        }
        if (data.complete_time === null){
            data.complete_time = ""
        }
        axios.put(`/kong/gongdi_mng/v1.0/gongdis/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                for(var item of getters.gongdis){
                    if(item.id === data.id){
                        var index = getters.gongdis.indexOf(item)
                        var [...newDatas] = getters.gongdis
                        newDatas.splice(index, 1, response.data)
                        commit('setGongdis',newDatas)
                        break
                    }
                }
            }
        })
    },
    removeGongdis({commit},data){
        axios.delete(`/kong/gongdi_mng/v1.0/gongdis/${data.id}`)
			.then(function(response){
                if(response.status === 204){
                    commit('removeGongdi',data)
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