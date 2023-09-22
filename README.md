# Batch-Data-Pipeline

# Introduction

In most business use case of cloud data engineering, we tends to design powerful architectures that meet their business needs, ensure **Availability, Scalability and Cost effectivness**, combining these 3 constraints proves difficult sometimes. 

**Persistent EMR Clusters** remain alive **all the time**, even when a job has completed, they have 2 major problems : 
- [ ] 1)It may result into **huge cost** due to idle time
- [ ] 2)when lot of heavy jobs run together then due to resource issue , the Spark Jobs might take **huge time** to complete in **Persistent EMR Cluster** , which might impact business ...

In this project, I'm gonna introduce the **Transient Cluster**  to resolve both issues: 
**launch fresh EMR Cluster when needed to run Spark Jobs & when the step is complete, the cluster get terminated automatically !** 

**Let's embark on the project to discover this solution !** 

# Architecture 
![Blank diagram](https://github.com/hafsaelgha/Batch-Data-Pipeline/assets/99973359/ec68c67a-a18f-4bc5-b10b-5da37baab97d)


