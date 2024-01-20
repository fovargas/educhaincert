workspace {

    model {
        // Actores externos
        institucionesEducativas = person "Instituciones Educativas" {
            tags "Microsoft Azure - Administrative Units"
        }
        
        participantes = person "Participantes" {
            tags "Microsoft Azure - Users"
        }
        
        empleadores = person "Empleadores y Organizaciones" {
            tags "Microsoft Azure - Ceres"
        }
        
        sga = softwareSystem "Sistemas de Gestión Académica" {
            tags "Microsoft Azure - Ceres"
        }

        // Sistema de microcredenciales
        sistemaMicrocredenciales = softwareSystem "Sistema de Gestión de Microcredenciales Universitarias" {
            
            // Contenedores dentro del sistema
            frontendApp = container "Frontend Application" "Aplicación web construida sobre Django. Permite a los usuarios interactuar con el sistema." {
                tags "Frontend Application" "Microsoft Azure - OS Images (Classic)"
            }
            backendApp = container "Backend Application" "Gestiona la lógica de negocios, incluyendo la emisión y verificación de microcredenciales." {
                tags "Backend Application" "Microsoft Azure - App Registrations"
            }
            database = container "Database" "Almacena información de credenciales, usuarios e interacciones." {
                tags "Backend Application Element" "Microsoft Azure - SQL Database"
            }
            blockchain = container "Blockchain" "Registra transacciones y microcredenciales de forma segura e inmutable." {
                tags "Backend Application Element" "Microsoft Azure - Azure Blockchain Service"
            }
            ipfs = container "IPFS" "Sistema de Archivos Interplanetarios para almacenamiento descentralizado." {
                tags "Backend Application Element" "Microsoft Azure - Quickstart Center"
            }
            did = container "Veramo" "Gestor de Identidades Descentralizadas" {
                tags "Backend Application Element" "Microsoft Azure - Identity Governance"
            }

            // Relaciones entre contenedores
            frontendApp -> backendApp "Envía solicitudes de usuario"
            backendApp -> database "Consulta y almacena datos"
            backendApp -> blockchain "Registra y verifica microcredenciales"
            backendApp -> ipfs "Almacena y recupera datos de microcredenciales"
            backendApp -> did "Gestiona identidades descentralizadas"

            // Relaciones de los usuarios con el sistema
            institucionesEducativas -> frontendApp "Usa"
            participantes -> frontendApp "Usa"
            empleadores -> frontendApp "Usa"
            sga -> frontendApp "Interactúa"
        }
    }

    views {
        container sistemaMicrocredenciales {
            include *
            autolayout lr
        }
        
        styles {
            element "Person" {
                background #edf2f4
            }
            
            element "Frontend Application" {
                background #d3f8e2
            }
            
            element "Backend Application" {
                background #2364aa
                color #ffffff
            }
            
            element "Backend Application Element" {
                background #b5e2fa
            }

        }

        theme https://static.structurizr.com/themes/microsoft-azure-2023.01.24/icons.json
    }

}