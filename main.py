import argparse
import sys
import subprocess

template = '''
db={db}
driver={driver}
conn={conn}
user={user}
password={password}

warehouses={warehouses}
loadWorkers={loadWorkers}

terminals={threads}
//To run specified transactions per terminal- runMins must equal zero
runTxnsPerTerminal={runTxnsPerTerminal}
//To run for specified minutes- runTxnsPerTerminal must equal zero
runMins={runMins}
//Number of total transactions per minute
limitTxnsPerMin={limitTxnsPerMin}

//Set to true to run in 4.x compatible mode. Set to false to use the
//entire configured database evenly.
terminalWarehouseFixed={terminalWarehouseFixed}

//The following five values must add up to 100
//The default percentages of 45, 43, 4, 4 & 4 match the TPC-C spec
newOrderWeight={newOrderWeight}
paymentWeight={paymentWeight}
orderStatusWeight={orderStatusWeight}
deliveryWeight={deliveryWeight}
stockLevelWeight={stockLevelWeight}

// Directory name to create for collecting detailed result data.
// Comment this out to suppress.
resultDirectory=my_result_%tY-%tm-%td_%tH%tM%tS
osCollectorScript=./misc/os_collector_linux.py
osCollectorInterval=1
//osCollectorSSHAddr=user@dbhost
//osCollectorDevices=net_eth0 blk_sda'''

# get flags from command line
parser = argparse.ArgumentParser(description='Run TPC-C benchmark')
parser.add_argument('--db', type=str, default='postgres', help='database type')
parser.add_argument('--driver', type=str, default='org.postgresql.Driver', help='JDBC driver class name to load')
parser.add_argument('--conn', type=str, default='jdbc:postgresql://localhost:5432/postgres', help='JDBC connection string')
parser.add_argument('--user', type=str, default='postgres', help='database user')
parser.add_argument('--password', type=str, default='postgres', help='database password')
parser.add_argument('--warehouses', type=int, default=1, help='overall database size scale factor')
parser.add_argument('--loadWorkers', type=int, default=4, help='number of parallel threads used to create the initial content')
parser.add_argument('--threads', type=int, default=1, help='number of parallel threads used to run the benchmark')
parser.add_argument('--runTxnsPerTerminal', type=int, default=0, help='number of transactions to run per thread')
parser.add_argument('--runMins', type=int, default=1, help='number of minutes to run the benchmark')
parser.add_argument('--limitTxnsPerMin', type=int, default=0, help='number of transactions to run per minute, 0 means unlimited')
parser.add_argument('--terminalWarehouseFixed', type=bool, default=True, help='Set to true to run in 4.x compatible mode. Set to false to use the entire configured database evenly.')
parser.add_argument('--newOrderWeight', type=int, default=45, help='percentage of newOrder transactions')
parser.add_argument('--paymentWeight', type=int, default=43, help='percentage of payment transactions')
parser.add_argument('--orderStatusWeight', type=int, default=4, help='percentage of orderStatus transactions')
parser.add_argument('--deliveryWeight', type=int, default=4, help='percentage of delivery transactions')
parser.add_argument('--stockLevelWeight', type=int, default=4, help='percentage of stockLevel transactions')
parser.add_argument('--mode', type=str, default='all', help='mode to run the benchmark, all, cleanup, prepare, run')


# exec shell script and print the output in real time
def run_shell(cmd):
    p = subprocess.Popen(cmd, stdout=sys.stdout.fileno(), stderr=sys.stderr.fileno(), shell=True)
    p.wait()


def main():
    args = parser.parse_args()
    # if the runTxnsPerTerminal is set, runMins must be 0
    if args.runTxnsPerTerminal != 0:
        args.runMins = 0

    # save config.properties in run directory
    with open('run/config.properties', 'w') as f:
        f.write(template.format(**vars(args)))

    if args.mode == 'all':
        # run cleanup, prepare and run

        # run runDatabaseDestroy.sh in run directory with config.properties
        run_shell('cd run && ./runDatabaseDestroy.sh config.properties')
    
        # run runDatabaseBuild.sh in run directory with config.properties
        run_shell('cd run && ./runDatabaseBuild.sh config.properties')

        # run runBenchmark.sh in run directory with config.properties
        run_shell('cd run && ./runBenchmark.sh config.properties')

    if args.mode == 'cleanup':
        # run cleanup

        # run runDatabaseDestroy.sh in run directory with config.properties
        run_shell('cd run && ./runDatabaseDestroy.sh config.properties')

    if args.mode == 'prepare':
        # run prepare

        # run runDatabaseBuild.sh in run directory with config.properties
        run_shell('cd run && ./runDatabaseBuild.sh config.properties')

    if args.mode == 'run':
        # run run

        # run runBenchmark.sh in run directory with config.properties
        run_shell('cd run && ./runBenchmark.sh config.properties')



if __name__ == '__main__':
    main()
