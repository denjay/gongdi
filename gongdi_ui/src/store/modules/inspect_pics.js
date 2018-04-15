import axios from 'axios'

const state = ()=>{
    return { inspect_pics:[] }
}

const getters = {
    inspect_pics:state=>{
        return state.inspect_pics
    },
}

const  mutations = {
    setInspectPics(state, data){
        state.inspect_pics = data
    },
    removeInspectPics(state,data){
        var index = state.inspect_pics.indexOf(data)
        state.inspect_pics.splice(index,1)
    },
}

const actions = {
    getInspectPics({commit},id){
        axios.get(`/kong/gongdi_mng/v1.0/inspects/${id}/pics`)
        .then(response=>{
            if(response.status === 200){
                commit('setInspectPics',response.data)
            }
        })
        .catch(function(error){
			alert('getInspectPics失败')
		})
    },
    removeInspectPics({commit},data){
        axios.delete(`/kong/gongdi_mng/v1.0/inspect_pics/${data.id}`)
        .then(function(response){
            if(response.status === 204){
                commit('removeInspectPics',data)
            }
        })
        .catch(function(error){
            alert('removeInspectPics失败')
        })
    }
}

export default {
    namespaced: true,    
    state,
    getters,
    mutations,
    actions,
}