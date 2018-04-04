<template>
  <div>
    <div class="">
      <el-collapse v-model="activeNames">
        <el-collapse-item title="可选筛选项" name="1">
          <div class="select">
            <span>选择部位：</span>
            <el-select v-model="insertData.companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
            <el-select v-model="insertData.dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
            <el-select v-model="insertData.buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
            <br>
            <span>文档名：</span>
            <el-input
              placeholder="请输入文档名"
              v-model="insertData.name"
              clearable>
            </el-input>
          </div>
        </el-collapse-item>
      </el-collapse>
      <el-button @click="getDocs" type="primary">查询</el-button>
      <el-button @click="insert" type="primary">新增文档</el-button>
    </div>

    <el-collapse v-model="activeNames">
      <el-collapse-item  v-for="item in doc_table" :key="item.index" :title="item.title" :name="item.name">
        <el-table
          :data="item.data"
          border
          style="width: 100%">
          <el-table-column
            fixed
            prop="code"
            label="编号"
            width="100">
          </el-table-column>
          <el-table-column
            prop="name"
            label="文档名"
            width="150">
          </el-table-column>
          <el-table-column
            prop="buwei_name"
            label="所属部位"
            width="150">
          </el-table-column>
          <el-table-column
            prop="description"
            label="描述">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="130">
            <template slot-scope="scope">
              <el-button @click="remove(scope.row)" size="mini" icon="el-icon-delete"></el-button>
              <el-button @click="edit(scope.row)" size="mini" icon="el-icon-edit"></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-collapse-item>
    </el-collapse>

    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <el-form label-position="right" label-width="100px" :model="insertData" :rules="rules" ref="ruleForm">
        <template v-if="title === '新增文档'">
          <el-form-item label="公司名称" prop="companyid">
            <el-select v-model="insertData.companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属单体" prop="dantiid">
            <el-select v-model="insertData.dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属部位" prop="buweiid">
            <el-select v-model="insertData.buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="文档类型" prop="doc_type">
            <el-select v-model="insertData.doc_type" filterable clearable placeholder="请选择文档类型">
              <el-option
                v-for="(val,key,index) in doc_types"
                :key="index"
                :label="key"
                :value="val">
              </el-option>
            </el-select>
          </el-form-item>
        </template>
        <el-form-item label="编号" prop="code">
          <el-input
            placeholder="请输入文档编号"
            v-model="insertData.code"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="文档名称" prop="name">
          <el-input
            placeholder="请输入文档名称"
            v-model="insertData.name"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            type="textarea"
            :rows="2"
            placeholder="请输入内容"
            v-model="insertData.description">
          </el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="resetForm('ruleForm')">取 消</el-button>
        <el-button type="primary" @click="submitForm('ruleForm')">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  export default {
    mounted(){
      this.$store.dispatch('guifan_tuzhi_tuji/buwei/getCompanies')
    },

    data() {
      return {
        rules: {
          companyid: [
            { required: true, message: '请选择所属公司', trigger: 'change' },
          ],
          dantiid: [
            { required: true, message: '请选择所属单体', trigger: 'change' },
          ],
          buweiid: [
            { required: true, message: '请选择所属部位', trigger: 'change' },
          ],
          doc_type: [
            { required: true, message: '请选择文档类型', trigger: 'change' },
          ],
          code: [
            { required: true, message: '请输入文件编码', trigger: 'blur' },
          ],
          name: [
            { required: true, message: '请输入文档名', trigger: 'blur' },
          ]
        },
        insertData:{
          companyid: '',
          dantiid: '',
          buweiid: null,
          doc_type: null,
          code: null,
          name: null, 
          description: '',
        },
        doc_types:{"规范管理":"guifang","图纸管理":"tuzhi","图集管理":"tuji"},
        doc_id: null,
        activeNames: ['1','2','3','4'],
        dialogVisible: false,
        title: '',
      }
    },

    methods: {
      getDocs(){
        this.$store.dispatch('guifan_tuzhi_tuji/getDocs', { "buwei":this.buwei_name, "doc_name":this.insertData.name })        
      },
      insert(){
        // 新增时先清空表单数据
        this.title = '新增文档'
        this.dialogVisible = true
        this.insertData.doc_type = ''
        this.insertData.name = ''
        this.insertData.code = ''
        this.insertData.description = ''
      },
      edit(data){
        // 点编辑时，将对应行数据写入表单
        this.title = '编辑文档'
        this.insertData.doc_type = data.doc_type
        this.doc_id = data.id
        this.insertData.name = data.name
        this.insertData.code = data.code
        this.insertData.description = data.description
        this.dialogVisible = true
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
        this.dialogVisible = false
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.submitData();
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      submitData(){
        // 组织表单需要的数据，创建或更新数据
        var data = {
          doc_type:this.insertData.doc_type,
          code:this.insertData.code,
          name:this.insertData.name,
          buweiid:this.insertData.buweiid,
          description:this.insertData.description,
        }
        if(this.title === '新增文档'){
          this.$store.dispatch('guifan_tuzhi_tuji/postDocs',data)
        }
        else if(this.title === '编辑文档'){
          console.log(data)
          data["id"] = this.doc_id
          delete data.buweiid          
          this.$store.dispatch('guifan_tuzhi_tuji/putDocs',data)
        }
        this.dialogVisible = false
      },
      remove(data) {
        this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
        }).then(() => {
          this.$store.dispatch('guifan_tuzhi_tuji/removeDocs',data);
        })
      },
      handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
      }
    },

    computed: {
      buwei_name(){
        if(Boolean(this.insertData.buweiid)){
          return this.buweis.filter(item => item.id === this.insertData.buweiid)[0]["name"]
        }
      },
      doc_table(){
        return [
          {title:"规范管理", name:"2", data:this.guifangs},
          {title:"图纸管理", name:"3", data:this.tuzhis},
          {title:"图集管理", name:"4", data:this.tujis},
        ]
      },
      ...mapGetters('guifan_tuzhi_tuji/buwei',{
        'dantis':'dantis',
        'companies':'companies',
        'buweis':'buweis',
        }
      ),
      ...mapGetters('guifan_tuzhi_tuji',{
        'guifangs':'guifangs',
        'tuzhis':'tuzhis',
        'tujis':'tujis',
		  }),
    },

    watch:{
      "insertData.companyid": function(){
        this.insertData.dantiid = ''
        this.$store.commit('guifan_tuzhi_tuji/buwei/setDantis',[])
        if(Boolean(this.insertData.companyid)){
          this.$store.dispatch('guifan_tuzhi_tuji/buwei/getDantis', this.insertData.companyid)
        }
      },
      "insertData.dantiid": function(){
        this.insertData.buweiid = null
        this.$store.commit('guifan_tuzhi_tuji/buwei/setBuweis',[])
        if(Boolean(this.insertData.dantiid)){
          this.$store.dispatch('guifan_tuzhi_tuji/buwei/getBuweis', this.insertData.dantiid)
        }
      },
    }     
  }
</script>

<style scoped>
  .select span {
    display:inline-block;
    width: 70px;
    font-size: 13px;
  }
  .select .el-select {
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
