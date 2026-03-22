/*
 * Jenkinsfile — Declarative Pipeline for Student Feedback Form (Sub-Task 5)
 *
 * Prerequisites on the Jenkins agent:
 *   - Python 3.x with pip
 *   - Google Chrome browser installed
 *   - Git (if pulling from a repository)
 */

pipeline {
    agent any

    environment {
        PYTHON = 'python'                       // Change to 'python3' on Linux/macOS
        PIP    = 'pip'                          // Change to 'pip3' on Linux/macOS
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm                    // Pulls code from the configured SCM (GitHub, etc.)
            }
        }

        stage('Setup') {
            steps {
                echo '🔧 Installing Python dependencies...'
                bat "${PIP} install -r tests/requirements.txt"
                // On Linux/macOS agents, replace 'bat' with 'sh'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo '🧪 Executing Selenium test suite...'
                bat "${PYTHON} -m pytest tests/test_feedback_form.py -v --tb=short --junitxml=reports/test-results.xml --html=reports/test-report.html --self-contained-html"
                // On Linux/macOS agents, replace 'bat' with 'sh'
            }
        }
    }

    post {
        always {
            echo '📊 Publishing test results...'

            // Publish JUnit test results
            junit allowEmptyResults: true, testResults: 'reports/test-results.xml'

            // Archive the HTML report
            archiveArtifacts artifacts: 'reports/test-report.html', allowEmptyArchive: true

            echo '✅ Pipeline complete.'
        }
        success {
            echo '🎉 All tests passed!'
        }
        failure {
            echo '❌ Some tests failed – check the report for details.'
        }
    }
}
