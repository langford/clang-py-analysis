// clang -cc1 -ast-dump example.m

#import <Foundation/Foundation.h>

static void test(void);

int main(int argc, char *argv[])
    {
    @autoreleasepool
        {
        test();
        NSLog(@"%@", @(42));
        }
    }

#pragma mark -

static void test(void)
    {
    if (1)
        {
        NSMutableDictionary *d = [NSMutableDictionary dictionaryWithObjects:@[] forKeys:@[]];
        [d setObject:@"yes" forKey:@"true"];
        NSLog(@"%@", d);
        }
    }
