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
    getBuweis(context,data){
        axios.get(`/kong/gongdi_mng/v1.0/dantis/${data}/buweis`)
        .then(response=>{
            if(response.status === 200){
                context.commit('setBuweis',response.data)
            }
        })
    },
    postBuwei(context,data){
        axios.post('/kong/gongdi_mng/v1.0/buweis',data)
		.then(response => {
            if (response.status === 201) {
                data = context.getters.buweis 
                data.unshift(response.data)
                context.commit('setBuweis', data)
            }
            else {
                alert('新增失败')
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putBuweis(context,data){
        console.table(data)
        delete data.danti_name
        delete data.dantiid
        axios.put(`/kong/gongdi_mng/v1.0/buweis/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                var i = 0, len = context.getters.dantis.length
                for(;i<len;i++){
                    if(context.getters.dantis[i].id === data.id){
                        var newDatas = context.getters.dantis
                        newDatas[i] = response.data 
                        context.commit('setDantis',newDatas)
                        // console.log(context.getters.dantis)
                        break
                    }
                }
            }
        })
        .catch(error => {
            alert('出错')
        })
    },
    removeBuweis(context,data){
        axios.delete(`/kong/gongdi_mng/v1.0/buweis/${data.id}`)
			.then(function(response){
                if(response.status === 204){
                    context.commit('removeBuweis',data)
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