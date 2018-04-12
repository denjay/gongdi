<template>
  <div>
    <div class="">
      <el-collapse v-model="activeNames">
        <el-collapse-item title="可选筛选项" name="1">
          <div class="select">
            <span>选择部位：</span>
            <el-select v-model="filterData.companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
            <el-select v-model="filterData.dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
            <el-select v-model="filterData.buweiid" filterable clearable placeholder="请选择部位">
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
              v-model="filterData.name"
              clearable>
            </el-input>
          </div>
        </el-collapse-item>
      </el-collapse>
      <el-button @click="getDocs(1)" type="primary">查询</el-button>
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

        <el-pagination
          v-show="Number(item.total_datas)"
          background
          layout="prev, pager, next"
          @current-change="(value) => handleCurrentChange(value, item.doc_type)"
          :page-size="page_size"
          :page-count="item.total_pages">
        </el-pagination>
      </el-collapse-item>
    </el-collapse>

    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <el-form label-position="right" label-width="100px" :model="formData" :rules="rules" ref="ruleForm">
        <template v-if="title === '新增文档'">
          <el-form-item label="公司名称" prop="companyid">
            <el-select v-model="formData.companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属单体" prop="dantiid">
            <el-select v-model="formData.dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属部位" prop="buweiid">
            <el-select v-model="formData.buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="文档类型" prop="doc_type">
            <el-select v-model="formData.doc_type" filterable clearable placeholder="请选择文档类型">
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
            v-model="formData.code"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="文档名称" prop="name">
          <el-input
            placeholder="请输入文档名称"
            v-model="formData.name"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            type="textarea"
            :rows="2"
            placeholder="请输入内容"
            v-model="formData.description">
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
        filterData:{
          companyid: '',
          dantiid: '',
          buweiid: null,
          name: null, 
        },
        formData:{
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
        page_size: 15,  
        guifang_cur_page:1,      
        tuzhi_cur_page:1,      
        tuji_cur_page:1,      
        activeNames: ['1','2','3','4'],
        dialogVisible: false,
        title: '',
      }
    },

    methods: {
      handleCurrentChange(val,type) {
        this.getDocs(val,[type])
        this[`${type}_cur_page`] = val
      },
      getDocs(page,doc_types=["guifang","tuzhi","tuji"]){
        this.$store.dispatch('guifan_tuzhi_tuji/getDocs', {"doc_types":doc_types, "page":page, "per_page":this.page_size, "buwei":this.buwei_name, "doc_name":this.filterData.name })        
      },
      insert(){
        // 新增时先清空表单数据
        this.title = '新增文档'
        this.dialogVisible = true
        this.formData.doc_type = ''
        this.formData.name = ''
        this.formData.code = ''
        this.formData.description = ''
      },
      edit(data){
        // 点编辑时，将对应行数据写入表单
        this.title = '编辑文档'
        this.formData.doc_type = data.doc_type
        this.doc_id = data.id
        this.formData.name = data.name
        this.formData.code = data.code
        this.formData.description = data.description
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
          doc_type:this.formData.doc_type,
          code:this.formData.code,
          name:this.formData.name,
          buweiid:this.formData.buweiid,
          description:this.formData.description,
        }
        if(this.title === '新增文档'){
          this.$store.dispatch('guifan_tuzhi_tuji/postDocs',data)
        }
        else if(this.title === '编辑文档'){
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
          // 删除一条数据之后的页数
          var total_pages =  Math.ceil((this[`${data.doc_type}_total_datas`]-1) / this.page_size)
          this.$store.dispatch('guifan_tuzhi_tuji/removeDocs',data);
          // 解决删除数据后，当前页大于总页数的问题
          var page = this[`${data.doc_type}_cur_page`] > total_pages ? total_pages : this[`${data.doc_type}_cur_page`];
          this.getDocs(page,[data.doc_type])
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
      guifang_total_pages(){
        return Math.ceil(this.guifang_total_datas / this.page_size)
      },
      tuzhi_total_pages(){
        return Math.ceil(this.tuzhi_total_datas / this.page_size)
      },
      tuji_total_pages(){
        return Math.ceil(this.tuji_total_datas / this.page_size)
      },
      // 根据buwiid取得部位名
      buwei_name(){
        if(Boolean(this.filterData.buweiid)){
          return this.buweis.filter(item => item.id === this.filterData.buweiid)[0]["name"]
        }
      },
      doc_table(){
        return [
          {title:"规范管理", name:"2", doc_type:"guifang", total_pages:this.guifang_total_pages, total_datas:this.guifang_total_datas, data:this.guifangs},
          {title:"图纸管理", name:"3", doc_type:"tuzhi", total_pages:this.tuzhi_total_pages, total_datas:this.tuzhi_total_datas, data:this.tuzhis},
          {title:"图集管理", name:"4", doc_type:"tuji", total_pages:this.tuji_total_pages, total_datas:this.tuji_total_datas, data:this.tujis},
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
        'guifang_total_datas':'guifang_total_datas',
        'tuzhi_total_datas':'tuzhi_total_datas',
        'tuji_total_datas':'tuji_total_datas',
		  }),
    },

    watch:{
      "filterData.companyid": function(){
        this.filterData.dantiid = ''
        this.$store.commit('guifan_tuzhi_tuji/buwei/setDantis',[])
        if(Boolean(this.filterData.companyid)){
          this.$store.dispatch('guifan_tuzhi_tuji/buwei/getDantis', {companyid:this.filterData.companyid})
        }
      },
      "filterData.dantiid": function(){
        this.filterData.buweiid = null
        this.$store.commit('guifan_tuzhi_tuji/buwei/setBuweis',[])
        if(Boolean(this.filterData.dantiid)){
          this.$store.dispatch('guifan_tuzhi_tuji/buwei/getBuweis', this.filterData.dantiid)
        }
      },
      "formData.companyid": function(){
        this.formData.dantiid = ''
        this.$store.commit('guifan_tuzhi_tuji/buwei/setDantis',[])
        if(Boolean(this.formData.companyid)){
          this.$store.dispatch('guifan_tuzhi_tuji/buwei/getDantis', {companyid:this.formData.companyid})
        }
      },
      "formData.dantiid": function(){
        this.formData.buweiid = null
        this.$store.commit('guifan_tuzhi_tuji/buwei/setBuweis',[])
        if(Boolean(this.formData.dantiid)){
          this.$store.dispatch('guifan_tuzhi_tuji/buwei/getBuweis', this.formData.dantiid)
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
