/*
Run dynamics analysis for NN learning BG prediction
test insulin levels and resultant change in reachability

For the HSCC 2020

-uses sherlock, gurobi

input arguments:
bolus_min := lower bound for initial insulin bolus range
bolus_max := upper bound for initial insulin bolus range
nn_test_name := network being tested
gluc_input_file := initial glucose trace
output_file_name := output file name


Taisa Kushner
taisa.kushner@colorado.edu

*/

#include "propagate_intervals.h"
#include <fstream>
#include <iostream>
using namespace std;
using namespace std::chrono;

int main(int argc, char ** argv)
{
	float bolus_min = -1;
	float bolus_max = -1;
	string nn_test_name ="";
	string gluc_input_file = "";
	string output_file_name="";

	char key[] = "all";

	if(argc != 6)
	{
		cout << "Wrong number of command line arguments : " << endl;
		cout << "Please pass the bolus_min, bolus_max, nn_test_name, gluc_input_file, output_file_name" << endl;
		cout << "Exiting... " << endl;
		exit(0);
	}

	else
	{
		sscanf(argv[1], "%d", &bolus_min);
		sscanf(argv[2], "%d", &bolus_max);
		nn_test_name = argv[3];
		gluc_input_file = argv[4];
		output_file_name=argv[5];
	}

	int num_insulin_inputs = 7;
	int num_other_inputs = 7;
	int bolus_location = 0;
	bool byLocation = true;
	bool byValue = false;
	ofstream output_file_stream(output_file_name);

	vector< vector< datatype > > input_interval(num_insulin_inputs+num_other_inputs, vector< datatype >(2,0));
	vector< vector< datatype > > input_constraints;
	clock_t begin, end;
	vector< datatype > output_range(2,0);
	// Simple range propagation
	// sherlock_parameters.verbosity = true;
	// sherlock_parameters.grad_search_point_verbosity = true;
	sherlock_parameters.time_verbosity = true;


	//char nn_test_name[] = "./BGnetworks/52104_GlucIns30_pred60_fullCons_10_APNN.nt" ;
	network_handler benchmark_BG(nn_test_name.c_str());


	// fill int glucose values from file
	//ifstream glucFile("glucInput2.csv");
	ifstream glucFile(gluc_input_file);
	string gluc_str = "";
 	float gluc_val = 0.0;
	float delta_per = 0.05;
	float delta = 0;

	for (int i=0; i<num_other_inputs; i++){
		getline(glucFile,gluc_str);
		gluc_val = std::atof(gluc_str.c_str());
		delta=abs(gluc_val)*delta_per;
		input_interval[i][0] = gluc_val-delta; input_interval[i][1]= gluc_val+delta;
	}
	glucFile.close();


if (byLocation){
	for (int n=0;n<num_insulin_inputs;n++){
		bolus_location=n;

		for (float m=0.0;m<10.0;m+=1.0){
		for (int i=num_other_inputs; i<num_insulin_inputs+num_other_inputs; i++){
			if (i == bolus_location+num_other_inputs){
				input_interval[i][0] = bolus_min+m; input_interval[i][1] = bolus_max+m;
			}
			else {
				input_interval[i][0] = 0; input_interval[i][1] = 0.05;
			}
		}

		//cout<<input_interval.size()<<" input constraint "<<input_constraints.size()<<endl;

		create_constraint_from_interval(input_constraints, input_interval);
		//cout<<input_constraints.size()<<endl;
		//cout<<input_interval[1][0]<<" "<<input_interval[1][1]<<endl;

		begin = clock();

		vector< vector< vector< datatype > > > weights;
		vector< vector< datatype > > biases;
		benchmark_BG.return_network_information(weights, biases);

		vector < datatype> upper_bound_vector;
		vector < datatype> lower_bound_vector;
		//output_range[1] = do_MILP_optimization(input_constraints, weights, biases, upper_bound_vector, 1);
		//output_range[0] = do_MILP_optimization(input_constraints, weights, biases, lower_bound_vector, -1);
		benchmark_BG.return_interval_output(input_constraints, output_range, 1);
		cout << "output_range = [" << output_range[0] << " , " << output_range[1] << " ]" << endl;
		end = clock();
		printf("time cost for Sherlock BG test ------------------ %lf\n", (double)(end - begin) / CLOCKS_PER_SEC);

		output_file_stream<<output_range[0]<<", "<<output_range[1]<<", ";
	}
	output_file_stream<<endl;
	}
	output_file_stream.close();
}

if (byValue){
	for (int n=0;n<num_insulin_inputs;n++){
		bolus_location=n;
		for (int i=num_other_inputs; i<num_insulin_inputs+num_other_inputs; i++){
			if (i == bolus_location+num_other_inputs){
				input_interval[i][0] = bolus_min; input_interval[i][1] = bolus_max;
			}
			else {
				input_interval[i][0] = 0; input_interval[i][1] = 0.05;
			}
		}


		//cout<<input_interval.size()<<" input constraint "<<input_constraints.size()<<endl;

		create_constraint_from_interval(input_constraints, input_interval);
		//cout<<input_constraints.size()<<endl;
		//cout<<input_interval[1][0]<<" "<<input_interval[1][1]<<endl;

		begin = clock();

		vector< vector< vector< datatype > > > weights;
		vector< vector< datatype > > biases;
		benchmark_BG.return_network_information(weights, biases);

		vector < datatype> upper_bound_vector;
		vector < datatype> lower_bound_vector;
		//output_range[1] = do_MILP_optimization(input_constraints, weights, biases, upper_bound_vector, 1);
		//output_range[0] = do_MILP_optimization(input_constraints, weights, biases, lower_bound_vector, -1);
		benchmark_BG.return_interval_output(input_constraints, output_range, 1);
		cout << "output_range = [" << output_range[0] << " , " << output_range[1] << " ]" << endl;
		end = clock();
		printf("time cost for Sherlock BG test ------------------ %lf\n", (double)(end - begin) / CLOCKS_PER_SEC);

		output_file_stream<<output_range[0]<<", "<<output_range[1]<<endl;
	}
	output_file_stream.close();
}
	// std::ofstream output_file("upperVector.txt");
	// for (int i=0;i<upper_bound_vector.size();i++){
	// 	output_file<<upper_bound_vector[i]<<endl;
	// }
	// output_file.close();
	//
	// std::ofstream output_file2("lowerVector.txt");
	// for (int i=0;i<lower_bound_vector.size();i++){
	// 	output_file2<<lower_bound_vector[i]<<endl;
	// }
	// output_file2.close();
	//
	// vector < vector < unsigned int > > active_weights;
	// cout<<compute_network_output(upper_bound_vector,weights,biases,active_weights)<<endl;

	return 0;
}
