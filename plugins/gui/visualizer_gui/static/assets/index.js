// dashboard vue Module implementation
function Module() {
    return({    
        data() {
            return { field_start_values }
          },
          methods: {
              increment() {
                this.count++
              }
          },
          compilerOptions: {
              // Initialize vue to have different delimiters to the ones used by jinja in flask: [[ , ]] 
              delimiters: ["[[", "]]"]
          }
    })
}

// define starting field values
function field_start_values(){
    return {
        count:0
    }
}
