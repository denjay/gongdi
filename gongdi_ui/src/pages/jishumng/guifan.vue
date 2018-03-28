<template>
  <div>
    <div class="">
      <el-collapse v-model="activeNames">
        <el-collapse-item title="可选筛选项" name="1">
          <div class="select">
            <span>请选择部位：</span>
            <el-select v-model="companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
            <el-select v-model="dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
            <el-select v-model="buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
            <br>
            <span>输入文档名：</span>
            <el-input
              placeholder="请输入文档名"
              v-model="name"
              clearable>
            </el-input>
          </div>
        </el-collapse-item>
      </el-collapse>
      <el-button @click="getGuifans" type="primary">查询</el-button>
      <el-button @click="insert" type="primary">新增规范</el-button>
    </div>

    <el-table
      :data="guifans"
      border
      style="width: 100%">
      <el-table-column
        fixed
        prop="code"
        label="编号"
        width="150">
      </el-table-column>
      <el-table-column
        prop="name"
        label="文档名">
        width="200"
      </el-table-column>
      <el-table-column
        prop="buwei_name"
        label="所属部位">
        width="200"
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
        width="100">
        <template slot-scope="scope">
          <el-button @click="remove(scope.row)" type="text" size="mini" icon="el-icon-delete"></el-button>
          <el-button @click="edit(scope.row)" type="text" size="mini" icon="el-icon-edit"></el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <el-form label-position="right" label-width="100px">
        <template v-if="title === '新增规范'">
          <el-form-item label="公司名称">
            <el-select v-model="companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属单体">
            <el-select v-model="dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属部位">
            <el-select v-model="buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
          </el-form-item>
        </template>
        <el-form-item label="编号">
          <el-input
            placeholder="请输入文档编号"
            v-model="code"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="文档名称">
          <el-input
            placeholder="请输入文档名称"
            v-model="name"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            type="textarea"
            :rows="2"
            placeholder="请输入内容"
            v-model="description">
          </el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitData">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  export default {
    mounted(){
      this.$store.dispatch('guifan/buwei/getCompanies')
    },

    data() {
      return {
        companyid: '',
        dantiid: '',
        buweiid: null,
        guifan_id: null,
        name: null, 
        code: null,
        description: '',
        activeNames: ['1'],
        dialogVisible: false,
        title: '',
      }
    },

    methods: {
      getGuifans(){
        this.$store.dispatch('guifan/getGuifans', { "buwei":this.buwei_name, "doc_name":this.name })        
      },
      insert(){
        this.title = '新增规范'
        this.dialogVisible = true
        this.name = ''
        this.code = ''
        this.description = ''
      },
      edit(data){
        this.title = '编辑规范'
        this.guifan_id = data.id
        this.name = data.name
        this.code = data.code
        this.description = data.description
        this.dialogVisible = true
      },
      submitData(){
        var data = {
          code:this.code,
          name:this.name,
          buweiid:this.buweiid,
          description:this.description,
        }
        if(this.title === '新增规范'){
          this.$store.dispatch('guifan/postGuifans',data)
        }
        else if(this.title === '编辑规范'){
          data["id"] = this.guifan_id
          delete data.buweiid          
          this.$store.dispatch('guifan/putGuifans',data)
        }
        this.dialogVisible = false
      },
      remove(data) {
        this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
        }).then(() => {
          this.$store.dispatch('guifan/removeGuifans',data);
        }).catch(() => {         
        });
      },
      handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
      }
    },

    computed: {
      buwei_name(){
        if(Boolean(this.buweiid)){
          return this.buweis.filter(item => item.id === this.buweiid)[0]["name"]
        }
      },
      ...mapGetters('guifan/buwei',{
        'dantis':'dantis',
        'companies':'companies',
        'buweis':'buweis',
        }
      ),
      ...mapGetters('guifan',{
        'guifans':'guifans',
		  }),
    },

    watch:{
      companyid: function(){
        this.dantiid = ''
        this.$store.commit('guifan/buwei/setDantis',[])
        if(Boolean(this.companyid)){
          this.$store.dispatch('guifan/buwei/getDantis', this.companyid)
        }
      },
      dantiid: function(){
        this.buweiid = null
        this.$store.commit('guifan/buwei/setBuweis',[])
        if(Boolean(this.dantiid)){
          this.$store.dispatch('guifan/buwei/getBuweis', this.dantiid)
        }
      },
    }     
  }
</script>

<style scoped>
  .el-select {
    width: 200px;
    margin-bottom: 20px;
  }
  .select {
    width: 700px;
    margin-right: 20px;
    display: inline-block;
  }
  .el-input {
    width: 200px;
    margin-bottom: 20px;
  }
  .el-form-item {
    margin-bottom: 0px;
  }
  .el-textarea {
    width: 200px;
  }
</style>

<style>
  .el-dialog {
    width: 385px !important;
  }
  .el-table {
    margin-top: 5px;
  }
  .el-collapse-item__header {
    width: 120px;
    font-size: 16px;
    color: #409eff;
  }
</style>
